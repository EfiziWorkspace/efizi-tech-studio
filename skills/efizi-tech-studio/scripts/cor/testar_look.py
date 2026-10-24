"""Aplica um look de looks.py num quadro do bruto (mesmo caminho do montar.grade) e mede.
Uso: python testar_look.py <look> [clip tempo cx y0]   saída: trabalho/cor_teste/<look>_<clip>.png"""

import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
from looks import LOOKS  # noqa: E402

look = sys.argv[1]
clip, t, cx, y0 = (sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 2 \
    else ("C2120", 63.45, 0.5, 420)
LUT = (AQUI / "slog3cine_to_rec709.cube").as_posix().replace(":", "\\:")
x0 = int(min(max(cx * 2160 - 900, 0), 2160 - 1800))
saida = RAIZ / "trabalho" / "cor_teste" / f"{look}_{clip}.png"
vf = (f"crop=1800:3200:{x0}:{y0},scale=1080:1920:in_color_matrix=bt709:in_range=tv:out_range=pc:flags=lanczos,"
      f"format=gbrp16le,lut3d=file='{LUT}':interp=tetrahedral,{LOOKS[look]},format=rgb24")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(RAIZ / "brutos" / f"{clip}.MP4"),
                "-frames:v", "1", "-vf", vf, str(saida)], check=True)
print(saida)
