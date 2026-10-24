# Fluxo completo, com comandos

Os comandos usam a versão do HyperFrames em que tudo isto foi testado: `npx --yes hyperframes@0.8.177`. Abaixo,
`hf` = esse comando. Python: 3.11+ com `numpy` e `pillow`. FFmpeg 7+ no PATH.

## 0. Projeto novo

```bash
python <skill>/scripts/novo_projeto.py videos/2026-10-24-assunto
```

Cria `brutos/ referencia/ cor/ trabalho/ composicao/ saida/`, copia os scripts, o `frame.md`, as fontes, a marca e o
encerramento, e gera a LUT técnica (`cor/gera_lut.py`).

## 1. Bruto

- Copiar tudo para `brutos/` (vídeo grande do Google Drive: baixar pelo navegador; o conector de arquivos costuma
  não baixar vídeo de GB).
- `ffprobe` em cada arquivo: duração, fps (23,976 = `24000/1001`), rotação (câmera na vertical grava 3840×2160 com
  rotação: o ffmpeg já gira), perfil de cor. Na Sony o perfil está no XML `NonRealTimeMeta` no fim do MP4
  (`CaptureGammaEquation = s-log3-cine`): imagem cinza e lavada = S-Log, precisa da LUT.
- Gravação de tela (OBS/Chrome) vai em `brutos/telas/`.

## 2. Transcrever

```bash
hf models install parakeet           # uma vez por máquina
hf transcribe brutos/C0001.MP4 --engine parakeet --language pt   # grava transcript.json ao lado
```

Copie o `transcript.json` de cada clipe para `trabalho/transcr/<clipe>/`. O ASR estica o fim da palavra até a
próxima e erra nome próprio ("efise" = Efizi, "gira" = Jira): os tempos de corte vêm da energia do áudio, não dele.

## 3. Takes → `trabalho/edl.json`

Ver `takes-e-cortes.md`. O EDL é a lista ordenada de cortes:

```json
{ "crop": {"w": 1800, "h": 3200},
  "enquadre": { "C0001": {"cx": 0.5, "y0": 420} },
  "cortes": [ {"id": "s01_gancho", "clip": "C0001", "in": 1.20, "out": 6.50, "look": "dourado",
               "texto": "A frase exata que ela fala neste corte."} ] }
```

`enquadre` = recorte vertical por câmera (centro x como fração de 2160 e topo em px do 4K vertical). `tipo: "tela"`
marca corte em que a câmera filma um monitor (pula recorte/quadro). `texto` é usado na conferência de voz.

## 4. ✋ Roteiro (`ROTEIRO.md`) — ver `retencao.md` e `efeitos-e-ritmo.md`

## 5. A-roll

```bash
cd trabalho
python montar.py grade      # cortes em quadros exatos + LUT + look -> cortes/grade/NN_id.mov
python montar.py recorte    # remove-background -> cortes/alpha/ (lento: ~2 min por 3 s)
python montar.py alfa       # conserta quadros em que o recorte perdeu o corpo -> cortes/alfa/
python montar.py quadro     # (opcional) redesenha o quadro branco do cenário -> cortes/quadro/
python montar.py tela       # cortes "tipo": "tela"
python montar.py juntar     # composicao/assets/video/aroll.mp4 + cortes/timeline.json
```

Cada etapa pula o arquivo que já existe. Mudou um corte? Tire **os arquivos daquele corte** de todas as pastas
(`grade/alpha/alfa/quadro/tela`) para uma pasta `antigo/` e rode de novo — e para cortes novos rode
`recorte(so=[i])` + `alfa(so=[i])` antes do `quadro`, senão ele trava esperando o alfa.

Sem recorte/quadro (vídeo simples)? `python montar.py previa` gera `aroll_previa.mp4` só com cor.

## 6. Telas, pessoa recortada, cenas

```bash
python telas.py     # clipes da gravação de tela (edite CLIPES)
python pessoa.py    # pessoa recortada com transparência para cenário atrás (edite TRECHOS e MESA)
```

## 7. Composição

`composicao/index.html` segue o contrato do HyperFrames (`hyperframes-core`). Use `exemplos/reels-agentes/index_modelo.html`
como base: as palavras da legenda entram no lugar de `/*PALAVRAS*/` a partir de um `v_palavras.js`
(`const W = [["Palavra", início, fim], ...]`, `*` na frente = palavra em destaque).

```bash
cd composicao
hf lint            # 0 erros
hf check
hf snapshot --at 1.5,6.4,25.3,42.5 --no-end --describe false -o ../trabalho/snap
```

## 8. Trilha

```bash
sh trabalho/sfx/gera_sfx.sh        # uma vez por projeto: sintetiza bolha, blip, plin, ding, vento e o drone
python trabalho/montar_trilha.py   # composicao/assets/trilha_e_efeitos.wav (música com sidechain + efeitos)
```

## 9. Render e conferência

```bash
cd composicao
hf render --fps 24000/1001 --quality delivery --no-best-effort -o ../saida/video.mp4
cd ../trabalho && python verif_audio.py ../saida/video.mp4
```

Ver `entrega.md` antes de mandar. Render de 75 s em 1080×1920: 6–9 min numa máquina com GPU.
