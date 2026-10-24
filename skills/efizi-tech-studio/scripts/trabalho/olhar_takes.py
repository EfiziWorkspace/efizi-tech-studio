"""Folha do olhar por take: uma imagem por candidato, 12 quadros por linha (um a cada 0,25 s), só o rosto.

EXEMPLO: o crop pega o rosto no 4K vertical desta câmera; ajuste para o enquadre da sua gravação.

Rodar: python olhar_takes.py saida.jpg CLIP:IN:OUT[:rotulo] ...
"""
import subprocess
import sys
import tempfile
from pathlib import Path

BRUTOS = Path(__file__).resolve().parent.parent / "brutos"
saida, specs = sys.argv[1], sys.argv[2:]
tmp = Path(tempfile.mkdtemp())
for k, spec in enumerate(specs):
    partes = spec.split(":")
    clip, a, b = partes[0], float(partes[1]), float(partes[2])
    n = int((b - a) / 0.25) + 1
    rows = (n + 11) // 12
    # vertical 2160x3840 depois da rotação; rosto da Lay fica em ~x 760–1520, y 1000–1560
    vf = f"fps=4,crop=760:560:760:1000,scale=200:-2,eq=contrast=1.5:saturation=1.4,tile=12x{rows}:padding=3:color=red"
    out = Path(saida.replace(".jpg", f"_{k}_{clip}_{a:g}.jpg"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", "-i", str(BRUTOS / f"{clip}.MP4"),
                    "-vf", vf, "-frames:v", "1", str(out)], check=True)
    print("ok", out)
