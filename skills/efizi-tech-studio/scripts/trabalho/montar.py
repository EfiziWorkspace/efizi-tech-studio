"""Montagem do A-roll: cenário real (zoom leve), cor (LUT técnica + look) e, se preciso, só o quadro branco redesenhado.

Cortes "tipo": "tela" (a câmera filmando o notebook) pulam recorte/alfa/quadro e levam desfoque do que não pode ir ao ar.

Etapas (cada uma pula o que já existe; apague a pasta da etapa para refazer):
  1 grade   : corte em quadros exatos -> recorte 1,2x -> LUT técnica S-Log3/S-Gamut3.Cine->709 -> look (efizi|tech)
              saída cortes/grade/NN_id.mov (ProRes 422 HQ + PCM)
  2 recorte : `hyperframes remove-background` em cada corte -> cortes/alpha/NN_id.mov (ProRes 4444 com alfa)
  3 alfa    : conserta quadros isolados em que o recorte perdeu o corpo -> cortes/alfa/NN_id.mkv
  4 quadro  : troca só a escrita do quadro branco pelo desenho novo (quadro.py) -> cortes/quadro/NN_id.mov
  5 tela    : desfoque do que não pode ir ao ar nos cortes de tela -> cortes/tela/ (juntar usa no lugar)
  6 juntar  : ../composicao/assets/video/aroll.mp4 (H.264, Rec.709) + cortes/timeline.json
Rodar: python montar.py [grade|recorte|alfa|quadro|tela|juntar|tudo]
"""

import json
import os

import numpy as np
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
BRUTOS = RAIZ / "brutos"
sys.path.insert(0, str(RAIZ / "cor"))
from looks import LOOKS  # noqa: E402

LUT = (RAIZ / "cor" / "slog3cine_to_rec709.cube").as_posix().replace(":", "\\:")
FPS = 24000 / 1001
V2 = AQUI / "cortes"  # pasta de trabalho (nome da variável mantido do montar_v3 do Reels Efizi Tech)
edl = json.loads((AQUI / "edl.json").read_text(encoding="utf-8"))
TELA = lambda c: c.get("tipo") == "tela"
CW, CH = edl["crop"]["w"], edl["crop"]["h"]
NPX = ["npx", "--yes", "hyperframes@0.8.177"]
REC709 = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


def nome(i, c):
    return f"{i:02d}_{c['id']}.mov"


def grade():
    (V2 / "grade").mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(edl["cortes"]):
        out = V2 / "grade" / nome(i, c)
        if out.exists():
            continue
        n = round((c["out"] - c["in"]) * FPS)
        dur = n / FPS
        enq = edl["enquadre"][c["clip"]]
        cw, ch = enq.get("w", CW), enq.get("h", CH)
        x0 = int(min(max(enq["cx"] * 2160 - cw / 2, 0), 2160 - cw))
        y0 = enq["y0"]
        vf = (
            f"crop={cw}:{ch}:{x0}:{y0},"
            "scale=1080:1920:in_color_matrix=bt709:in_range=tv:out_range=pc:flags=lanczos,"
            f"format=gbrp16le,lut3d=file='{LUT}':interp=tetrahedral,"
            f"{LOOKS[c['look']]},format=yuv422p10le"
        )
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{c['in']:.3f}", "-i", str(BRUTOS / f"{c['clip']}.MP4"),
             "-t", f"{dur:.4f}", "-vf", vf, "-r", "24000/1001", "-frames:v", str(n),
             "-c:v", "prores_ks", "-profile:v", "3", *REC709,
             "-af", f"afade=t=in:d=0.012,afade=t=out:st={dur - 0.012:.4f}:d=0.012", "-ac", "2", "-ar", "48000",
             "-c:a", "pcm_s16le", str(out)],
            check=True,
        )
        print("grade", out.name, n, "quadros")


def recorte(so=None):
    (V2 / "alpha").mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(edl["cortes"]):
        out = V2 / "alpha" / nome(i, c)
        if out.exists() or TELA(c) or (so is not None and i not in so):
            continue
        subprocess.run([*NPX, "remove-background", str(V2 / "grade" / nome(i, c)), "-o", str(out)],
                       check=True, shell=(os.name == "nt"), stdout=subprocess.DEVNULL)
        print("recorte", out.name)


def alfa(so=None):
    """Conserta quadros isolados em que o recorte perde o corpo (mão rápida com borrão de movimento).

    Quadro com cobertura do alfa < 95% da mediana do corte recebe o alfa do vizinho bom mais perto.
    Mantém a contagem de quadros (o tmedian do ffmpeg come 2 quadros e desalinha a legenda).
    Saída: v2/alfa/NN_id.mkv (FFV1, cinza 8 bits).
    """
    import numpy as np

    (V2 / "alfa").mkdir(parents=True, exist_ok=True)
    W, H = 1080, 1920
    for i, c in enumerate(edl["cortes"]):
        out = V2 / "alfa" / nome(i, c).replace(".mov", ".mkv")
        if out.exists() or TELA(c) or (so is not None and i not in so):
            continue
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(V2 / "alpha" / nome(i, c)), "-vf", "alphaextract,format=gray",
             "-f", "rawvideo", "-"], check=True, capture_output=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(-1, H, W).copy()
        cob = a.reshape(len(a), -1).mean(axis=1)
        # falha = queda isolada contra a vizinhança (±6 quadros), não contra o corte todo: braço que entra e sai
        # do quadro muda a cobertura de verdade, e congelar o alfa ali deixaria o desenho do quadro sobre o braço
        viz6 = np.array([np.median(cob[max(0, k - 6):k + 7]) for k in range(len(cob))])
        ruins = set(np.nonzero(cob < 0.93 * viz6)[0].tolist())
        bons = [k for k in range(len(a)) if k not in ruins]
        for k in sorted(ruins):
            viz = min(bons, key=lambda b: (abs(b - k), b > k))  # empate: o anterior
            a[k] = a[viz]
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}",
             "-r", "24000/1001", "-i", "-", "-c:v", "ffv1", str(out)],
            input=a.tobytes(), check=True)
        print("alfa", out.name, len(a), "quadros, consertados:", sorted(ruins))


def quadro(so=None):
    """so: índices dos cortes a processar (padrão: todos)."""
    from quadro import Quadro

    (V2 / "quadro").mkdir(parents=True, exist_ok=True)
    W, H = 1080, 1920
    tam = W * H * 3 * 2
    for i, c in enumerate(edl["cortes"]):
        out = V2 / "quadro" / nome(i, c)
        if out.exists() or TELA(c) or (so is not None and i not in so):
            continue
        q = Quadro(c["clip"])
        # a matriz tem de ser dita nos dois sentidos, ou o swscale usa a BT.601 e a cor muda
        cor = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(V2 / "grade" / nome(i, c)),
                                "-vf", "scale=in_color_matrix=bt709:in_range=tv:out_range=pc", "-f", "rawvideo",
                                "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)
        alf = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(V2 / "alfa" / nome(i, c).replace(".mov", ".mkv")),
                                "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
        enc = subprocess.Popen(
            ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", "24000/1001",
             "-i", "-", "-i", str(V2 / "grade" / nome(i, c)), "-map", "0:v", "-map", "1:a",
             "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv422p10le",
             "-c:v", "prores_ks", "-profile:v", "3", *REC709, "-c:a", "copy", str(out)],
            stdin=subprocess.PIPE)
        k = 0
        while True:
            b = cor.stdout.read(tam)
            a = alf.stdout.read(W * H)
            if len(b) < tam or len(a) < W * H:
                break
            rgb = np.frombuffer(b, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535.0
            alfa = np.frombuffer(a, np.uint8).reshape(H, W).astype(np.float32) / 255.0
            if k == 0:
                q.ajustar_placa(rgb, alfa)  # câmera parada: a superfície do quadro sai do 1º quadro de cada corte
            novo = q.aplicar(rgb, alfa, semente=i * 10000 + k)
            enc.stdin.write((np.clip(novo, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes())
            k += 1
        enc.stdin.close()
        enc.wait(); cor.wait(); alf.wait()
        print("quadro", out.name, k, "quadros")


def tela():
    """Cortes "tipo": "tela": desfoca as caixas de "desfoque" do corte ([x, y, w, h, t0, t1] em px do quadro final e
    s do corte; t1 = null vai até o fim). Saída: cortes/tela/NN_id.mov (juntar usa no lugar do quadro)."""
    (V2 / "tela").mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(edl["cortes"]):
        out = V2 / "tela" / nome(i, c)
        if not TELA(c) or out.exists():
            continue
        caixas = c.get("desfoque", [])
        fc, ult = "[0:v]null[v0];", "v0"
        for k, (x, y, w, h, t0, t1) in enumerate(caixas):
            quando = f"between(t,{t0},{t1})" if t1 is not None else f"gte(t,{t0})"
            fc += (f"[{ult}]split[a{k}][b{k}];[b{k}]crop={w}:{h}:{x}:{y},boxblur=22:3[c{k}];"
                   f"[a{k}][c{k}]overlay={x}:{y}:enable='{quando}'[v{k + 1}];")
            ult = f"v{k + 1}"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(V2 / "grade" / nome(i, c)), "-filter_complex", fc.rstrip(";"),
             "-map", f"[{ult}]", "-map", "0:a", "-c:v", "prores_ks", "-profile:v", "3", *REC709, "-c:a", "copy", str(out)],
            check=True)
        print("tela", out.name, len(caixas), "caixas")


def juntar(pasta="quadro", saida="aroll.mp4"):
    lista = V2 / f"lista_{pasta}.txt"
    def fonte(i, c):  # corte de tela (etapa tela) entra no lugar do quadro
        return V2 / "tela" / nome(i, c) if TELA(c) and pasta == "quadro" else V2 / pasta / nome(i, c)
    lista.write_text("".join(f"file '{fonte(i, c).as_posix()}'\n" for i, c in enumerate(edl["cortes"])), encoding="utf-8")
    dst = RAIZ / "composicao" / "assets" / "video" / saida
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", *REC709,
         # o concat de ProRes perde primárias e transferência; grava as três no próprio H.264
         "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
         # o concat deixa brechas de ~7 ms entre os cortes; quem lê o áudio em sequência (o render do HyperFrames)
         # junta as brechas e a voz adianta até 0,13 s no fim. Preencher com silêncio deixa o áudio contínuo e exato.
         "-af", "aresample=async=1:min_hard_comp=0.001:first_pts=0",
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(dst)],
        check=True,
    )
    tl, t = [], 0.0
    for c in edl["cortes"]:
        d = round((c["out"] - c["in"]) * FPS) / FPS
        tl.append({"id": c["id"], "start": round(t, 4), "dur": round(d, 4), "look": c["look"], "texto": c["texto"]})
        t += d
    (V2 / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=2), encoding="utf-8")
    print("juntar", dst.name, round(t, 3), "s")


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if etapa in ("grade", "tudo"):
        grade()
    if etapa == "previa":
        grade()
        juntar("grade", "aroll_previa.mp4")
    if etapa in ("recorte", "tudo"):
        recorte()
    if etapa in ("alfa", "tudo"):
        alfa()
    if etapa in ("quadro", "tudo"):
        quadro()
    if etapa in ("tela", "tudo"):
        tela()
    if etapa in ("juntar", "tudo"):
        juntar()
