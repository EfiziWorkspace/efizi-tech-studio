"""Cria a pasta de um vídeo novo com tudo que o fluxo da skill usa.

Uso: python novo_projeto.py videos/2026-10-24-assunto [--sem-lut]

Cria brutos/ referencia/ cor/ trabalho/ composicao/ saida/, copia os scripts da montagem, o frame.md, a marca,
as fontes, o encerramento padrão e o exemplo de composição, e gera a LUT técnica S-Log3 -> Rec.709 em cor/.
"""

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
if len(sys.argv) < 2:
    sys.exit(__doc__)
destino = Path(sys.argv[1]).resolve()
if destino.exists() and any(destino.iterdir()):
    sys.exit(f"{destino} já existe e não está vazia — escolha outro nome.")

for pasta in ["brutos/telas", "referencia", "cor", "trabalho/musica", "trabalho/transcr", "composicao/compositions",
              "composicao/assets/video", "saida"]:
    (destino / pasta).mkdir(parents=True, exist_ok=True)

shutil.copytree(SKILL / "scripts" / "trabalho", destino / "trabalho", dirs_exist_ok=True)
shutil.copytree(SKILL / "scripts" / "cor", destino / "cor", dirs_exist_ok=True)
shutil.copytree(SKILL / "modelos" / "composicao", destino / "composicao", dirs_exist_ok=True)
shutil.copy(SKILL / "modelos" / "frame.md", destino / "composicao" / "frame.md")
shutil.copy(SKILL / "modelos" / "encerramento" / "outro-efizi-tech.html", destino / "composicao" / "compositions")
exemplo = SKILL / "exemplos" / "reels-agentes"
shutil.copy(exemplo / "index_modelo.html", destino / "trabalho" / "index_modelo.html")
shutil.copy(exemplo / "edl.json", destino / "trabalho" / "edl.exemplo.json")
(destino / "trabalho" / "musica" / "LEIA.txt").write_text(
    "Ponha aqui a música de fundo (.mp3 ou .wav) com licença de uso. O montar_trilha.py usa a primeira.\n",
    encoding="utf-8")
nome = destino.name
(destino / "composicao" / "meta.json").write_text(json.dumps(
    {"id": nome, "name": nome, "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")},
    ensure_ascii=False, indent=2), encoding="utf-8")

if "--sem-lut" not in sys.argv:
    subprocess.run([sys.executable, "gera_lut.py"], cwd=destino / "cor", check=True)

print(f"pronto: {destino}")
print("próximos passos: copie a gravação para brutos/, transcreva e monte o trabalho/edl.json "
      "(veja references/fluxo.md)")
