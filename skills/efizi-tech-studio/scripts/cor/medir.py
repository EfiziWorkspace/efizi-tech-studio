"""Mede a cor de um quadro: tons (p2/p50/p98 da luma), saturação, tinta das sombras/médios/altas (a*, b* do Lab)
e a pele (caixa x0,y0,x1,y1 em pixels). Uso: python medir.py imagem.png [x0 y0 x1 y1]"""

import sys

import numpy as np
from PIL import Image


def lab(rgb):
    c = np.where(rgb > 0.04045, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    m = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.9505, 1.0, 1.089])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


img = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float64) / 255
L = lab(img)
y = L[..., 0]
sat = (img.max(-1) - img.min(-1)) / (img.max(-1) + 1e-6)
p2, p50, p98 = np.percentile(y, [2, 50, 98])
print(f"luma L*: p2 {p2:.1f}  p50 {p50:.1f}  p98 {p98:.1f}   saturação média {sat.mean():.3f}  p90 {np.percentile(sat, 90):.3f}")
for nome, a, b in [("sombras", 0, 30), ("médios", 30, 70), ("altas", 70, 101)]:
    m = (y >= a) & (y < b)
    print(f"{nome:8s} ({m.mean() * 100:4.1f}%): a* {L[..., 1][m].mean():+5.1f}  b* {L[..., 2][m].mean():+5.1f}")
if len(sys.argv) == 6:
    x0, y0, x1, y1 = map(int, sys.argv[2:])
    p = L[y0:y1, x0:x1].reshape(-1, 3)
    h = np.degrees(np.arctan2(p[:, 2], p[:, 1]))
    print(f"pele: L* {p[:, 0].mean():.1f}  a* {p[:, 1].mean():+.1f}  b* {p[:, 2].mean():+.1f}  "
          f"croma {np.hypot(p[:, 1], p[:, 2]).mean():.1f}  matiz {np.median(h):.0f}°")
