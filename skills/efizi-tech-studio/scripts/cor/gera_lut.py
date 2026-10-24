"""LUT técnica Sony S-Log3 / S-Gamut3.Cine -> Rec.709 (SDR, gama 2.4), sem "look".

Metadados da câmera (XML NonRealTimeMeta dentro do MP4, Sony ILCE-7M4):
  CaptureGammaEquation = s-log3-cine, CaptureColorPrimaries = s-gamut3-cine, CodingEquations = rec709.

Cadeia (tudo pelas fórmulas publicadas pela Sony e pela ITU):
  1. código de vídeo (faixa legal 64–940 em 10 bits) -> S-Log3 -> reflectância linear da cena
  2. S-Gamut3.Cine -> Rec.709 por matriz 3x3 calculada das primárias (branco D65 nos dois)
  3. tom de cena -> tela: curva com ombro suave (preserva as altas luzes em vez de cortar)
  4. Rec.709 / BT.1886: codifica com gama 1/2.4
A entrada do .cube é RGB 0–1 vindo do ffmpeg com in_range=tv (0 = código 64, 1 = código 940).

Rodar: python gera_lut.py   -> grava slog3cine_to_rec709.cube nesta pasta.
"""

from pathlib import Path

import numpy as np

N = 65
AQUI = Path(__file__).resolve().parent

# exposição: 18% de cinza da cena vai para ~0,42 na tela (meio-tom do Rec.709)
EXPOSICAO = 1.0
# ombro da curva: quanto maior, mais altas luzes cabem antes de saturar
BRANCO_CENA = 9.0


def slog3_para_linear(code10):
    """Fórmula oficial Sony S-Log3 (código 10 bits -> reflectância linear)."""
    code10 = np.asarray(code10, dtype=np.float64)
    out = np.where(
        code10 >= 171.2102946929,
        (10.0 ** ((code10 - 420.0) / 261.5)) * (0.18 + 0.01) - 0.01,
        (code10 - 95.0) * 0.01125000 / (171.2102946929 - 95.0),
    )
    return out


def rgb_para_xyz(prim, branco):
    xr, yr = prim[0]
    xg, yg = prim[1]
    xb, yb = prim[2]
    xw, yw = branco
    X = lambda x, y: np.array([x / y, 1.0, (1 - x - y) / y])
    M = np.stack([X(xr, yr), X(xg, yg), X(xb, yb)], axis=1)
    W = X(xw, yw)
    S = np.linalg.solve(M, W)
    return M * S


D65 = (0.3127, 0.3290)
SGAMUT3_CINE = [(0.766, 0.275), (0.225, 0.800), (0.089, -0.087)]
REC709 = [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)]
M_SG3C_709 = np.linalg.inv(rgb_para_xyz(REC709, D65)) @ rgb_para_xyz(SGAMUT3_CINE, D65)


def _filmico(v):
    # curva fílmica de referência (ajuste de Narkowicz da RRT/ODT do ACES): pé e ombro suaves
    return (v * (2.51 * v + 0.03)) / (v * (2.43 * v + 0.59) + 0.14)


def curva_tom(x):
    """Curva fílmica aplicada na luminância (preserva matiz e pele); excesso de cor clara vai para o branco."""
    x = np.maximum(x, 0.0)
    lum = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]
    lum_t = np.clip(_filmico(lum), 0, 1)
    escala = lum_t / np.maximum(lum, 1e-9)
    y = x * escala[..., None]
    # canal que passar de 1 (cor clara muito saturada): mistura com o branco mantendo a luminância
    pico = np.max(y, axis=-1, keepdims=True)
    lum_y = (0.2126 * y[..., 0] + 0.7152 * y[..., 1] + 0.0722 * y[..., 2])[..., None]
    t = np.clip((pico - 1.0) / np.maximum(pico - lum_y, 1e-9), 0, 1)
    y = y + (lum_y - y) * t
    return np.clip(y, 0, 1)


def calibrar_exposicao():
    """Acha o ganho que leva o cinza 18% para 0,42 depois da curva + gama 2.4."""
    alvo = 0.42**2.4
    lo, hi = 0.1, 20.0
    for _ in range(60):
        g = (lo + hi) / 2
        v = curva_tom(np.array([[0.18 * g] * 3]))[0, 0]
        lo, hi = (g, hi) if v < alvo else (lo, g)
    return (lo + hi) / 2


def main():
    ganho = calibrar_exposicao() * EXPOSICAO
    eixo = np.linspace(0, 1, N)
    # ordem do .cube: R varia mais rápido
    b, g, r = np.meshgrid(eixo, eixo, eixo, indexing="ij")
    rgb = np.stack([r, g, b], axis=-1).reshape(-1, 3)
    code = 64.0 + rgb * 876.0
    lin = slog3_para_linear(code)
    lin709 = lin @ M_SG3C_709.T
    tela = curva_tom(lin709 * ganho)
    saida = np.power(tela, 1 / 2.4)
    with open(AQUI / "slog3cine_to_rec709.cube", "w", encoding="ascii") as f:
        f.write('TITLE "Sony S-Log3 S-Gamut3.Cine to Rec.709 (tecnica, sem look)"\n')
        f.write(f"LUT_3D_SIZE {N}\n")
        for v in saida:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    print("matriz S-Gamut3.Cine -> Rec.709:\n", np.round(M_SG3C_709, 6))
    print("ganho de exposicao:", round(ganho, 4))
    for nome, c in [("preto (95)", 95), ("cinza 18% (420)", 420), ("branco 90% (598)", 598), ("pico (940)", 940)]:
        l = slog3_para_linear(c)
        y = curva_tom(np.array([[l * ganho] * 3]))[0, 0] ** (1 / 2.4)
        print(f"  {nome}: linear {l:.4f} -> tela {y:.3f}")


if __name__ == "__main__":
    main()
