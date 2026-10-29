"""Monta uma versão mantendo o HDR do iPhone (HLG, BT.2020, 10 bits), sem passar por SDR.
Cada corte é codificado à parte (HEVC Main10, mesmos parâmetros) e depois tudo é juntado sem recodificar —
abrir 30+ vídeos 4K num processo só estoura a memória. Vídeo SDR (exportado/WhatsApp) é levado para HLG com o
branco no nível de referência (~75%), sem tonemap. Uso: python montar_hdr.py v1|v2 <brutos> <saida.mp4>"""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import edl

versao, RAW, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
EDL = getattr(edl, "TEASER", []) + (edl.V1 if versao == "v1" else edl.V2)
FPS_NUM, FPS_DEN = 60000, 1001
W, H = 2160, 3840
AMBIENTE_LUFS = -30.0 if versao == "v1" else -31.0
VOZ_LUFS = -16.0
GANHO_MAX = 18.0
PASTA = os.path.join(os.path.dirname(SAIDA), "segmentos")
os.makedirs(PASTA, exist_ok=True)
X265 = ("colorprim=bt2020:transfer=arib-std-b67:colormatrix=bt2020nc:range=limited:"
        "repeat-headers=1:pools=4:frame-threads=2:log-level=error")


def transfer(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=color_transfer", "-of", "csv=p=0", f], capture_output=True, text=True)
    return r.stdout.strip().strip(",").split(",")[0]


def lufs(f, a, b):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", f,
                        "-map", "0:a:0", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -70.0


def segmento(c):
    f, a, b, o = c
    src = os.path.join(RAW, f)
    n = round((b - a) * FPS_NUM / FPS_DEN)
    dur = n * FPS_DEN / FPS_NUM
    chave = hashlib.md5(json.dumps([f, a, b, o, AMBIENTE_LUFS]).encode()).hexdigest()[:10]
    vid, wav = os.path.join(PASTA, f"{chave}.mp4"), os.path.join(PASTA, f"{chave}.wav")
    pre = ""
    if o.get("girar"):  # vídeo gravado deitado: gira e recorta em pé, centrado em cx (fração da largura)
        pre = f"{o['girar']},crop=ih*9/16:ih:iw*{o['cx']}-ih*9/32:0,"
    hlg = transfer(src) == "arib-std-b67"
    if hlg:
        cor = pre + f"scale={W}:{H}:flags=lanczos,format=yuv420p10le"
    else:  # SDR Rec.709 -> HLG BT.2020, branco do SDR em ~75% do sinal (BT.2408)
        cor = (pre + f"zscale=w={W}:h={H}:filter=lanczos:rin=tv:t=linear,format=gbrpf32le,exposure=exposure=1.2,"
               "zscale=p=bt2020:t=arib-std-b67:m=bt2020nc:r=tv,format=yuv420p10le")
    if not os.path.exists(vid):
        vf = (f"{cor},setsar=1,fps={FPS_NUM}/{FPS_DEN},trim=end_frame={n},setpts=PTS-STARTPTS,"
              "setparams=color_primaries=bt2020:color_trc=arib-std-b67:colorspace=bt2020nc:range=tv")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "2", "-ss", f"{a:.3f}", "-t", f"{b - a + 0.5:.3f}",
                        "-i", src, "-map", "0:v:0", "-vf", vf, "-frames:v", str(n),
                        "-c:v", "libx265", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p10le",
                        "-profile:v", "main10", "-x265-params", X265, "-tag:v", "hvc1",
                        "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc",
                        "-color_range", "tv", "-video_track_timescale", "60000", vid + ".tmp.mp4"], check=True)
        os.rename(vid + ".tmp.mp4", vid)
    voz = o.get("voz", False)
    ga = max(-30, min(GANHO_MAX, (VOZ_LUFS if voz else AMBIENTE_LUFS) - lufs(src, a, b)))
    if not os.path.exists(wav):
        af = ("aresample=48000,aformat=channel_layouts=stereo,highpass=f=70," + ("afftdn=nf=-30," if voz else "") +
              f"volume={ga:.1f}dB,afade=t=in:d={0.008 if voz else 0.03},afade=t=out:st={dur - 0.03:.4f}:d=0.03,"
              f"apad=whole_dur={dur:.6f},atrim=0:{dur:.6f}")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a + 0.5:.3f}", "-i", src,
                        "-map", "0:a:0", "-af", af, "-c:a", "pcm_s24le", wav], check=True)
    return f"{f:26s} {a:6.2f}-{b:6.2f} {'HLG' if hlg else 'SDR->HLG'} {ga:+.1f} dB", vid, wav, dur


res = []
for i, c in enumerate(EDL):  # um corte por vez: 4K HEVC + filtros em float usam muita memória
    res.append(segmento(c))
    print(f"{i:02d} {res[-1][0]}", flush=True)

lista = SAIDA + ".lista.txt"
open(lista, "w").write("".join(f"file '{v}'\n" for _, v, _, _ in res))
audio = SAIDA + ".audio.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y"] + sum((["-i", w] for _, _, w, _ in res), []) +
               ["-filter_complex", "".join(f"[{i}:a]" for i in range(len(res))) +
                f"concat=n={len(res)}:v=0:a=1,alimiter=limit=0.89:level=false[a]", "-map", "[a]",
                "-c:a", "pcm_s24le", audio], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-i", audio,
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-tag:v", "hvc1", "-c:a", "aac", "-b:a", "192k",
                "-shortest", "-movflags", "+faststart", SAIDA], check=True)
print(f"{len(res)} cortes, {sum(r[3] for r in res):.2f} s\nok {SAIDA}")
