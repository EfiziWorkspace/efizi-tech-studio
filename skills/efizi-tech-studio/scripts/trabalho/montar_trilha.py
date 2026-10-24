"""Trilha + efeitos (a voz fica no A-roll; isto é só o que vai por baixo dela).

EXEMPLO do Reels "agentes de IA" — troque DUR, TELAS e EFEITOS pelos tempos do seu vídeo.
- Música: o primeiro .mp3/.wav em trabalho/musica/ (com licença de uso), repetida com crossfade de 2 s.
- Efeitos: biblioteca do HyperFrames + sintetizados em trabalho/sfx (gera_sfx.sh). "meu:x" = sfx/x.wav.
- Música baixa e abaixada pela voz (sidechain): ouve-se nas pausas, some sob a fala; sobe no encerramento.
Saída: ../composicao/assets/trilha_e_efeitos.wav (48 kHz, estéreo).
"""

import os
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
# biblioteca de efeitos das skills do HyperFrames: clone ao lado do projeto ou skills instaladas no Claude/agents
_CAND = [AQUI.parents[2] / "hyperframes" / "skills", Path.home() / ".claude" / "skills", Path.home() / ".agents" / "skills"]
SFX = next((c / "media-use" / "audio" / "assets" / "sfx" for c in _CAND if (c / "media-use" / "audio" / "assets" / "sfx").is_dir()),
           Path(os.environ.get("HF_SFX", "sfx-nao-encontrado")))
MUSICA = next(iter(sorted((AQUI / "musica").glob("*.mp3")) + sorted((AQUI / "musica").glob("*.wav"))), None)
assert MUSICA, "ponha a música em trabalho/musica/"
SAIDA = AQUI.parent / "composicao" / "assets" / "trilha_e_efeitos.wav"
DUR = 75.024  # duração total do vídeo = data-duration do #root na composição


# Só efeito com motivo: o 3D do gancho, o avatar do Ultron, cada chicote de tela (entra e sai),
# os dois cliques que aparecem na tela, a chamada e o encerramento. Nada nos selos e fluxos
# (feedback: "cheio de som de clique e coin aleatório, tem que fazer sentido").
TELAS = [(14.95, 2.45), (24.95, 4.2), (32.15, 3.0), (38.0, 5.45), (55.55, 6.59)]  # (entra, duração), igual ao index
EFEITOS = [
    (1.40, "whoosh", -18), (1.76, "sparkle", -16),                 # biodigestor 3D surge e gira no dedo
    # ULTRON: sobe a tensão, glitch abre o mundo apocalíptico com impacto grave e drone sombrio; glitch fecha
    (4.62, "riser", -12, 2.2, 0.85), (5.38, "glitch-1", -12, 0, 0.3), (5.46, "impact-bass-1", -22),
    (5.46, "meu:drone_apoc", -15), (5.75, "meu:ding", -21),          # ding: avatar sai da ponta do dedo
    (8.51, "glitch-2", -14, 0, 0.25),
    # 1º "eles aprendem sozinhos": glitch, problema (erro), aprendizado salvo (chime no "sozinhos"), glitch de volta
    (10.51, "glitch-3", -15, 0, 0.25), (10.65, "error", -19), (12.0, "chime", -16), (12.93, "glitch-1", -18, 0, 0.2),
    # 2º: cérebro nascendo (brilho)
    (45.38, "glitch-3", -15, 0, 0.25), (45.9, "sparkle", -12), (47.97, "glitch-1", -18, 0, 0.2),
    (64.40, "glitch-2", -16, 0, 0.25),                            # virada para a cultura AI First
    *[e for t0, d in TELAS for e in ((t0, "whoosh-short", -15), (t0 + d - 0.3, "whoosh-short", -17))],
    (27.50, "click-soft", -15),                                    # clique no card do Jira (na gravação)
    (42.42, "click-soft", -12),                                    # "é só clicar aqui": o mouse clica no botão
    (68.35, "whoosh", -18),                                        # chamada: tela divide
    # encerramento padrão (sub-composição em 72,2)
    (72.22, "whoosh-cinematic", -6),
    (72.87, "key-press", -16), (72.95, "key-press", -16), (73.03, "key-press", -16), (73.11, "key-press", -16),
    (73.42, "whoosh-short", -18), (73.80, "click-soft", -14),
    (73.84, "meu:bolha", -6), (73.84 + 0.16, "meu:bolha2", -6),
]

# música baixa (-14 dB antes do sidechain) e abaixada pela própria voz (sidechain com o áudio do A-roll):
# sob a fala cai ~12 dB e some; nas pausas volta. No encerramento, sem voz, sobe a -11 dB.
MUSICA_DB = "volume='if(lt(t,72.024),0.1995,0.2818)':eval=frame"
VOZ = AQUI.parent / "composicao" / "assets" / "video" / "aroll.mp4"

entradas = ["-i", str(MUSICA), "-i", str(MUSICA), "-i", str(VOZ)]
filtros = [f"[0:a][1:a]acrossfade=d=2:c1=tri:c2=tri,atrim=0:{DUR},asetpts=N/SR/TB,aresample=48000,{MUSICA_DB},"
           f"afade=t=out:st={DUR - 1.2}:d=1.2[m0]",
           f"[2:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={DUR}[voz]",
           "[m0][voz]sidechaincompress=threshold=0.012:ratio=8:attack=25:release=300:knee=4[m]"]
rotulos = ["[m]"]
for i, (t, nome, db, *corte) in enumerate(EFEITOS, start=3):
    arq = AQUI / "sfx" / f"{nome[4:]}.wav" if nome.startswith("meu:") else SFX / f"{nome}.mp3"
    entradas += ["-i", str(arq)]
    ms = int(t * 1000)
    # (tempo, efeito, dB[, de, duração]): pedaço do efeito, com fade de 30 ms na saída
    rec = (f"atrim={corte[0]}:{corte[0] + corte[1]},asetpts=N/SR/TB,afade=t=out:st={corte[1] - 0.03}:d=0.03,"
           if corte else "")
    filtros.append(f"[{i}:a]{rec}aresample=48000,aformat=channel_layouts=stereo,volume={db}dB,adelay={ms}|{ms}[e{i}]")
    rotulos.append(f"[e{i}]")
filtros.append(f"{''.join(rotulos)}amix=inputs={len(rotulos)}:normalize=0:duration=first,atrim=0:{DUR}[out]")

subprocess.run(
    ["ffmpeg", "-y", "-v", "error", *entradas, "-filter_complex", ";".join(filtros), "-map", "[out]",
     "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(SAIDA)],
    check=True,
)
print("ok:", SAIDA)
