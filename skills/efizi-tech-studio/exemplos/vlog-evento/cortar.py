"""Etapa 1: cada corte vira um intermediário ProRes 422 HQ 10 bits, 1080x1920, 30 fps, SDR Rec.709.
HDR (HLG do iPhone) é convertido com tonemap; SDR só é redimensionado. Uso: python cortar.py <raw> <saida>"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from edl import V1, V2

RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
FPS = 30

def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=color_transfer", "-of", "json", f], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0].get("color_transfer", "")

def nome(c):
    f, a, b, o = c
    z = f"_z{o['zoom']}" if o.get("zoom") else ""
    z += f"_t{o['tela'][0]}-{o['tela'][1]}" if o.get("tela") else ""
    return f"{os.path.splitext(f)[0]}_{a:.2f}_{b:.2f}{z}.mov"

def cortar(c):
    f, a, b, o = c
    dst = os.path.join(OUT, nome(c))
    if os.path.exists(dst):
        return dst
    src = os.path.join(RAW, f)
    n = round((b - a) * FPS)
    zoom = o.get("zoom")
    pre = ""
    if zoom:  # recorte na parte de cima da tela (fora do texto pequeno do rodapé)
        pre = f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})/2:ih*0.10,"
    if probe(src) == "arib-std-b67":
        cv = (pre + "zscale=w=1080:h=1920:filter=lanczos:t=linear:npl=203,format=gbrpf32le,"
              "zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,"
              "zscale=t=bt709:m=bt709:r=tv,format=yuv422p10le")
    else:
        cv = pre + "scale=1080:1920:flags=lanczos:out_color_matrix=bt709,format=yuv422p10le"
    vf = f"fps={FPS},{cv},setsar=1"
    if o.get("tela"):  # só a faixa (y0..y1) da tela no centro, fundo = a mesma faixa desfocada e escurecida
        y0, y1 = o["tela"]
        faixa = f"crop=iw:ih*{y1 - y0}:0:ih*{y0}"
        vf += (f",split[a][b];[a]{faixa},scale=1080:-2[fg];"
               f"[b]{faixa},scale=-2:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.12[bg];"
               "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv422p10le")
    af = "aresample=48000,aformat=channel_layouts=stereo"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", src, "-map", "0:v:0", "-map", "0:a:0",
           "-vf", vf, "-af", af, "-frames:v", str(n), "-t", f"{n / FPS:.6f}",
           "-c:v", "prores_ks", "-profile:v", "3", "-c:a", "pcm_s16le",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", dst + ".tmp.mov"]
    subprocess.run(cmd, check=True)
    os.rename(dst + ".tmp.mov", dst)
    return dst

cortes = {nome(c): c for c in V1 + V2}
with ThreadPoolExecutor(2) as ex:
    for d in ex.map(cortar, cortes.values()):
        print("ok", os.path.basename(d), flush=True)
