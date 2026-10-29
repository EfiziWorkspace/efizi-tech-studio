"""Etapa 2: mede cada corte (cor e volume), iguala tudo e junta numa versão final.
Uso: python montar.py v1|v2 <cortes> <saida.mp4>"""
import json, math, os, re, statistics, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from edl import V1, V2
from cortar_nome import nome

versao, CORTES, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
EDL = V1 if versao == "v1" else V2
FPS = 30
NOITE = ("ida5", "ida6", "volta1", "volta2")      # cenas noturnas/telas: não puxar exposição
AMBIENTE_LUFS = -30.0 if versao == "v1" else -31.0  # som ambiente baixo, por baixo da narração/música
VOZ_LUFS = -16.0
GANHO_MAX = 18.0
SAT_GLOBAL = float(os.environ.get("SAT_GLOBAL", "0.8"))

def medir_cor(f):
    cache = f + ".cor.json"
    if os.path.exists(cache):
        return json.load(open(cache))
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf",
                        "scale=270:480,format=yuv420p,signalstats,metadata=print:file=-", "-f", "null", "-"],
                       capture_output=True, text=True)
    vals = {}
    for k in ("YAVG", "UAVG", "VAVG", "SATAVG", "YLOW", "YHIGH"):
        xs = [float(x) for x in re.findall(rf"lavfi\.signalstats\.{k}=([\d.]+)", r.stdout)]
        vals[k] = statistics.fmean(xs)
    json.dump(vals, open(cache, "w"))
    return vals

def medir_lufs(f):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -70.0

cortes = []
for c in EDL:
    f = os.path.join(CORTES, nome(c))
    cortes.append({"c": c, "f": f, "cor": medir_cor(f), "lufs": medir_lufs(f),
                   "noite": c[0].split(".")[0] in NOITE, "voz": c[3].get("voz", False)})

dia = [x for x in cortes if not x["noite"]]
alvo_y = statistics.median(x["cor"]["YAVG"] for x in dia)
alvo_sat = statistics.median(x["cor"]["SATAVG"] for x in dia)
alvo_u = statistics.median(x["cor"]["UAVG"] for x in dia)
alvo_v = statistics.median(x["cor"]["VAVG"] for x in dia)
clamp = lambda v, lo, hi: max(lo, min(hi, v))

filtros, rel = [], []
for i, x in enumerate(cortes):
    k = x["cor"]
    # exposição: gama que leva a média de luma 60% do caminho até o alvo (só cenas de dia)
    g = 1.0
    if not x["noite"]:
        y, t = k["YAVG"] / 255, (k["YAVG"] + 0.6 * (alvo_y - k["YAVG"])) / 255
        g = clamp(math.log(y) / math.log(t), 0.9, 1.15)
    # tinta: tira 60% do desvio de U/V em relação à mediana do dia (máx. 6 níveis em 8 bits)
    du = clamp(0.6 * (k["UAVG"] - alvo_u), -6, 6) * 4
    dv = clamp(0.6 * (k["VAVG"] - alvo_v), -6, 6) * 4
    s = clamp(1 + 0.6 * (alvo_sat / max(k["SATAVG"], 1) - 1), 0.8, 1.0) * SAT_GLOBAL
    v = ("format=yuv422p10le,"
         f"lutyuv=u='clip(val-({du:.1f}),0,1023)':v='clip(val-({dv:.1f}),0,1023)',"
         f"eq=gamma={g:.3f}:saturation={s:.3f}:contrast=1.04,"
         "unsharp=5:5:0.25:5:5:0,setpts=PTS-STARTPTS")
    alvo_a = VOZ_LUFS if x["voz"] else AMBIENTE_LUFS
    ga = clamp(alvo_a - x["lufs"], -30, GANHO_MAX)
    dur = round((x["c"][2] - x["c"][1]) * FPS) / FPS
    a = ("highpass=f=70," + ("afftdn=nf=-30," if x["voz"] else "") +
         f"volume={ga:.1f}dB,afade=t=in:d={0.008 if x['voz'] else 0.03},afade=t=out:st={dur - 0.03:.3f}:d=0.03,"
         f"atrim=0:{dur:.6f},asetpts=PTS-STARTPTS")
    filtros.append(f"[{i}:v]{v}[v{i}];[{i}:a]{a}[a{i}]")
    rel.append(f"{i:02d} {os.path.basename(x['f']):34s} Y {k['YAVG']:6.1f} gama {g:.2f} sat {s:.2f} "
               f"dU {du/4:+.1f} dV {dv/4:+.1f} | {x['lufs']:6.1f} LUFS -> {ga:+.1f} dB")

n = len(cortes)
fc = ";".join(filtros) + ";" + "".join(f"[v{i}][a{i}]" for i in range(n)) + \
     f"concat=n={n}:v=1:a=1[vc][ac];[vc]format=yuv420p[vo];" \
     "[ac]aresample=48000:async=1:first_pts=0,alimiter=limit=0.89:level=false[ao]"
cmd = ["ffmpeg", "-v", "error", "-y"]
for x in cortes:
    cmd += ["-i", x["f"]]
cmd += ["-filter_complex", fc, "-map", "[vo]", "-map", "[ao]", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-maxrate", "10M", "-bufsize", "20M",
        "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", SAIDA]
print("\n".join(rel))
print(f"alvo Y {alvo_y:.1f} sat {alvo_sat:.1f} U {alvo_u:.1f} V {alvo_v:.1f}")
subprocess.run(cmd, check=True)
print("ok", SAIDA)
