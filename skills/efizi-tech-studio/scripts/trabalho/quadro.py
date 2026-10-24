"""Troca só o que está escrito no quadro branco atrás da pessoa; o resto do cenário fica como foi gravado.

EXEMPLO: REGIAO é o polígono do quadro branco em cada câmera — meça no 1º quadro com uma grade de 100 px.

Em cada quadro (1080x1920, já cortado e com a cor final):
  1. placa limpa: superfície do quadro ajustada por um polinômio de 2º grau nos pixels visíveis do quadro
     (fora da pessoa e fora da escrita antiga, que cai como resíduo alto), com grão da câmera por cima;
  2. desenho novo (quadro/arte_<setup>.png) aplicado em "multiplicar", levemente desfocado como o quadro real;
  3. a pessoa volta na frente pelo alfa do recorte. Pixel escuro (cabelo, camisa) nunca é trocado, mesmo
     se o recorte falhar num quadro.
Rodar sozinho para testar numa foto: python quadro.py foto.png alfa.png C2116 saida.png
"""

import subprocess
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
W, H = 1080, 1920

# superfície do quadro em cada câmera (polígono em px do quadro final, medido em grade de 100 px),
# com margem para dentro das bordas e abaixo do apagador preso no topo
REGIAO = {
    # Reels da Lay: medido em grade de 100 px no 1º quadro de cada câmera (enquadre do edl.json)
    "C2118": [(0, 160), (930, 160), (930, 930), (0, 930)],
    "C2120": [(60, 150), (1080, 150), (1080, 900), (60, 900)],
    "C2121": [(46, 146), (1080, 146), (1080, 900), (46, 900)],
    "C2122": [(46, 146), (1030, 146), (1030, 930), (46, 930)],
    "C2123": [(64, 226), (1010, 226), (1010, 920), (64, 920)],
    "C2124": [(70, 226), (1014, 226), (1014, 920), (70, 920)],
    "C2125": [(140, 216), (1080, 216), (1080, 900), (140, 900)],
}


def _ler_rgba(caminho):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(caminho), "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 4).astype(np.float32) / 255.0


def _desfoque(img, r):
    """Desfoque de caixa separável (3 passadas ~ gaussiano) com somas acumuladas."""
    out = img.astype(np.float32)
    for _ in range(3):
        for eixo in (0, 1):
            pad = [(0, 0)] * out.ndim
            pad[eixo] = (r + 1, r)
            c = np.cumsum(np.pad(out, pad, mode="edge"), axis=eixo)
            n = out.shape[eixo]
            out = (np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=eixo)
                   - np.take(c, np.arange(0, n), axis=eixo)) / (2 * r + 1)
    return out


def _poligono(pts):
    yy, xx = np.mgrid[0:H, 0:W]
    dentro = np.ones((H, W), bool)
    n = len(pts)
    for i in range(n):  # polígono convexo, sentido horário: dentro = à direita de cada aresta
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        dentro &= (x2 - x1) * (yy - y1) - (y2 - y1) * (xx - x1) >= 0
    return dentro


class Quadro:
    def __init__(self, setup):
        self.setup = setup
        reg = _poligono(REGIAO[setup]).astype(np.float32)
        self.regiao = np.clip(_desfoque(reg, 3), 0, 1)  # borda macia de ~6 px
        arte = _ler_rgba(AQUI / "quadro" / f"arte_{setup}.png")
        a = arte[..., 3:4]
        # o quadro real está um pouco fora de foco: desfoca o desenho na mesma medida
        a = _desfoque(a, 1)
        cor = _desfoque(arte[..., :3] * arte[..., 3:4], 1) / np.maximum(a, 1e-4)
        self.mult = 1.0 - 0.94 * a + 0.94 * a * cor  # fator de "multiplicar" (1 = sem tinta)
        yy, xx = np.mgrid[0:H:4, 0:W:4]
        self._grade = (xx.astype(np.float32) / W, yy.astype(np.float32) / H)
        self.placa = None

    @staticmethod
    def _termos(x, y):
        return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y], axis=-1)

    def ajustar_placa(self, rgb, alfa):
        """Ajusta a superfície limpa a partir de um quadro (rgb 0–1, HxWx3) e do alfa da pessoa (0–1, HxW)."""
        s = (slice(0, H, 4), slice(0, W, 4))
        reg = self.regiao[s] > 0.99
        pessoa = _desfoque((alfa[s] > 0.02).astype(np.float32), 4) > 0.01  # ~16 px de folga em volta do cabelo
        lum = rgb[s].mean(-1)
        ok = reg & ~pessoa & (lum > 0.4)
        x, y = self._grade[0][ok], self._grade[1][ok]
        A = self._termos(x, y)
        cores = rgb[s][ok]
        for _ in range(3):  # a escrita antiga sai como resíduo alto e é descartada
            coef, *_ = np.linalg.lstsq(A, cores, rcond=None)
            res = np.abs(A @ coef - cores).max(-1)
            manter = res < 0.025
            A, cores = A[manter], cores[manter]
        yy, xx = np.mgrid[0:H, 0:W]
        self.placa = (self._termos(xx.astype(np.float32) / W, yy.astype(np.float32) / H) @ coef).astype(np.float32)
        return int(ok.sum()), int(manter.sum())

    def aplicar(self, rgb, alfa, semente):
        rng = np.random.default_rng(semente)
        grao = rng.normal(0, 0.008, (H, W, 1)).astype(np.float32)
        novo = np.clip((self.placa + grao) * self.mult, 0, 1)
        lum = rgb.mean(-1)
        escuro = np.clip((lum - 0.30) / 0.12, 0, 1)  # cabelo e camisa nunca são trocados
        m = (self.regiao * (1.0 - alfa) * escuro)[..., None]
        return rgb * (1 - m) + novo * m


if __name__ == "__main__":
    foto, alfa_png, setup, saida = sys.argv[1:5]
    img = _ler_rgba(foto)
    alfa = _ler_rgba(alfa_png)[..., 3]
    q = Quadro(setup)
    print("pixels do quadro usados no ajuste:", q.ajustar_placa(img[..., :3], alfa))
    out = (q.aplicar(img[..., :3], alfa, 0) * 255 + 0.5).astype(np.uint8)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", saida],
                   input=out.tobytes(), check=True)
    print("ok", saida)
