"""Conferência da voz antes de entregar (feedback: "verifica essas coisas antes de me entregar").

1. Emendas: em cada troca de corte do A-roll, mede a voz nos 40 ms antes e depois. Voz alta colada no corte
   (> -32 dB) = palavra picotada ou ataque seco — sai como ALERTA.
2. Texto: retranscreve o vídeo final (parakeet) e compara, corte a corte, com o texto do edl.json; palavra
   repetida, faltando ou trocada sai na lista.
Uso: python verif_audio.py [video]   (padrão: ../saida/reels-lay-agentes.mp4)
"""

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
VIDEO = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI.parent / "saida" / "reels-lay-agentes.mp4"
TMP = AQUI / "verif" / "audio"
TMP.mkdir(parents=True, exist_ok=True)
SR = 16000

raw = TMP / "voz.raw"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQUI.parent / "composicao" / "assets" / "video" / "aroll.mp4"),
                "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", str(raw)], check=True)
voz = np.fromfile(raw, np.int16) / 32768
db = lambda s: 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-9)

linha = json.loads((AQUI / "cortes" / "timeline.json").read_text(encoding="utf-8"))
print("1) emendas do A-roll (voz 40 ms antes | depois do corte)")
alertas = 0
for a, b in zip(linha, linha[1:]):
    t = b["start"]
    i = int(t * SR)
    antes, depois = db(voz[i - 640:i]), db(voz[i:i + 640])
    ruim = antes > -32 or depois > -32
    alertas += ruim
    print(f"  {t:7.3f}  {a['id']:>14} -> {b['id']:<14} {antes:6.1f} | {depois:6.1f}  {'ALERTA' if ruim else 'ok'}")

print("\n2) texto falado x roteiro")
wav = TMP / "final.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vn", "-ac", "1", "-ar", str(SR), str(wav)], check=True)
subprocess.run("npx --yes hyperframes@0.8.177 transcribe final.wav --engine parakeet --language pt", cwd=TMP, shell=True,
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ouvido = json.loads((TMP / "transcript.json").read_text(encoding="utf-8"))
norm = lambda w: re.sub(r"[^\wà-ú]", "", w.lower())
edl = json.loads((AQUI / "edl.json").read_text(encoding="utf-8"))
diferencas = 0
for c, seg in zip(edl["cortes"], linha):
    t0, t1 = seg["start"], seg["start"] + seg["dur"]
    esperado = [norm(w) for w in c["texto"].split()]
    falado = [norm(w["text"]) for w in ouvido if t0 - 0.05 <= w["start"] < t1 - 0.05]
    ops = [o for o in difflib.SequenceMatcher(a=esperado, b=falado).get_opcodes() if o[0] != "equal"]
    if ops:
        diferencas += 1
        print(f"  {c['id']:>14}: roteiro '{' '.join(esperado)}'\n  {'':>14}  ouvido  '{' '.join(falado)}'")
print("\n3) sincronia voz x boca: áudio do vídeo final contra o bruto de cada corte (correlação)")
fora = 0
for c, seg in zip(edl["cortes"], linha):
    d = min(1.5, seg["dur"] - 0.4)
    ler = lambda src, ss, t: np.frombuffer(subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(t), "-i", str(src), "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
        capture_output=True, check=True).stdout, np.int16).astype(float)
    a = ler(VIDEO, seg["start"] + 0.2, d)
    b = ler(AQUI.parent / "brutos" / f"{c['clip']}.MP4", c["in"] + 0.2 - 0.3, d + 0.6)
    sc = [np.dot(a, b[k:k + len(a)]) / (np.linalg.norm(b[k:k + len(a)]) + 1e-9) for k in range(len(b) - len(a))]
    ms = (int(np.argmax(sc)) / 8000 - 0.3) * 1000
    fora += abs(ms) > 40
    print(f"  {c['id']:>14} {seg['start']:7.3f}  {ms:+5.0f} ms  {'FORA' if abs(ms) > 40 else 'ok'}")
print(f"\n{alertas} emenda(s) com voz no corte; {diferencas} corte(s) com texto diferente (o ASR erra nomes: conferir à mão); "
      f"{fora} corte(s) fora de sincronia (> 40 ms)")
