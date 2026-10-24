"""Clipes das gravações de tela da Lay (brutos/telas, 1280×720, 30 fps) para as entradas de tela do Reels.

EXEMPLO: troque REC pela sua gravação e CLIPES pelos trechos (início, fim) em segundos que vão ao ar.

Corta a barra do Chrome (88 px do topo: abas e endereço), sobe para 1920 px de largura com lanczos
(o zoom da composição chega a 1,9×) e grava a 24000/1001, sem áudio — a voz é a do A-roll.
Cada clipe pode juntar mais de um trecho (o Jira pula os 3 s de carregamento do card).
Saída: ../composicao/assets/video/tela_<id>.mp4
"""

import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REC = AQUI.parent / "brutos" / "telas" / "2026-10-21 13-05-06.mp4"
DST = AQUI.parent / "composicao" / "assets" / "video"

# id: trechos (início, fim) em segundos da gravação
CLIPES = {
    "repos": [(69.0, 71.45)],                    # lista de repositórios descendo até "Corrige sozinho"
    "jira": [(145.30, 148.15), (150.85, 152.2)],  # cursor indo ao card, clique, card aberto
    "lalita": [(216.0, 219.0)],                  # página da Lalita
    "criar": [(272.0, 277.45)],                  # Agentes, com o botão Criar agente
    "aprende": [(322.4, 329.0)],                 # Lalita › Aprendizados, rolando a lista
}

for nome, trechos in CLIPES.items():
    partes = []
    for k, (a, b) in enumerate(trechos):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[p{k}]")
    junta = "".join(f"[p{k}]" for k in range(len(trechos)))
    filtro = ";".join(partes) + f";{junta}concat=n={len(trechos)}:v=1:a=0,crop=1280:632:0:88," \
             "scale=1920:948:flags=lanczos,fps=24000/1001,format=yuv420p[v]"
    saida = DST / f"tela_{nome}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(REC), "-filter_complex", filtro, "-map", "[v]",
                    "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-g", "12", "-an", str(saida)], check=True)
    print("ok:", saida.name, sum(b - a for a, b in trechos))
