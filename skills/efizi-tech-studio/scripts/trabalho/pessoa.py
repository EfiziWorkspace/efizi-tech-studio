"""A Lay recortada (vídeo com transparência, VP9 + alfa) para pôr cenário ATRÁS dela na composição.

EXEMPLO: troque TRECHOS (corte, câmera, de, até) e MESA (borda da mesa por câmera, medida num quadro).

Parte do corte já pronto (cortes/quadro, com cor e quadro redesenhado) e do alfa consertado (cortes/alfa):
- o alfa é "apertado" 3 px e suavizado, para não sobrar a borda clara da parede em volta dela no cenário escuro;
- tudo abaixo da borda da mesa continua opaco (mesa e notebook ficam; só a parede e o quadro somem).
Saída: ../composicao/assets/video/pessoa_<nome>.webm, do quadro `de` ao `ate` do corte (relativo ao corte).
"""

import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CORTES = AQUI / "cortes"
DST = AQUI.parent / "composicao" / "assets" / "video"
FPS = 24000 / 1001

# borda da mesa por câmera: reta (x0, y0) -> (x1, y1) no quadro 1080×1920; abaixo dela fica o vídeo original
MESA = {"C2120": (0, 1170, 1080, 1390), "C2124": (0, 1215, 1080, 1490)}

# nome: (corte, câmera, de, até) em segundos dentro do corte
TRECHOS = {
    "ultron": ("01_s02_ultron", "C2120", 0.15, 3.30),
    "sozinhos": ("02_s03_sozinhos", "C2120", 0.0, 2.419),
    "prometi": ("12_s11_prometi", "C2124", 2.20, 4.796),
}

for nome, (corte, cam, de, ate) in TRECHOS.items():
    x0, y0, x1, y1 = MESA[cam]
    f0, f1 = round(de * FPS), round(ate * FPS)
    # máscara da mesa: 255 abaixo da reta, rampa de 24 px
    reta = f"(Y-({y0}+({y1}-{y0})*X/{x1}))"
    mesa = f"clip(128+{reta}*255/24,0,255)"
    fc = (f"[0:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS,format=yuv420p[c];"
          f"[1:v]trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS,format=gray,"
          f"erosion,erosion,erosion,gblur=sigma=1.5,geq=lum='max(lum(X,Y),{mesa})'[a];"
          "[c][a]alphamerge,format=yuva420p[v]")
    saida = DST / f"pessoa_{nome}.webm"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(CORTES / "quadro" / f"{corte}.mov"),
                    "-i", str(CORTES / "alfa" / f"{corte}.mkv"), "-filter_complex", fc, "-map", "[v]",
                    "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "10M", "-auto-alt-ref", "0",
                    "-row-mt", "1", "-an", str(saida)], check=True)
    print("ok:", saida.name, f1 - f0, "quadros")
