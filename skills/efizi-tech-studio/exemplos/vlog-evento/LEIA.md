# Vlog de evento (celular, HDR) — dia 1 do AI Brasil Experience 2026

Exemplo de vlog montado só com ffmpeg (sem HyperFrames): 30 clipes de iPhone, duas versões (uma para
narrar por cima e outra só com música), sem legenda nem encerramento. Os vídeos ficam fora do repositório.

## O que cada arquivo faz

| Arquivo | Papel |
| --- | --- |
| `edl.py` | lista de cortes das duas versões (`V1` narrada ~67 s, `V2` música ~52 s), na ordem do dia |
| `cortar.py` | cada corte → ProRes 422 HQ 10 bits, 1080×1920, 30 fps, SDR Rec.709 |
| `montar.py` | iguala o volume de cada corte e junta: `python montar.py v1 cortes/ saida/v1.mp4` (`IGUALAR=1` liga a correção de cor por corte) |
| `transcrever.py` | faster-whisper `medium` em pt, com tempo por palavra (para escolher a fala e o ponto de corte) |

## Lições deste vídeo

- **iPhone grava HLG (HDR)**; misturado com vídeo SDR (exportado do app, WhatsApp) a cor fica diferente.
  Converter com `zscale … npl=203 → tonemap=mobius:param=0.3:desat=0 → bt709` deixou natural; `hable` ficou
  escuro e "só marcar como bt709" ficou lavado.
- **Igualar por número:** média de luma/saturação/tinta (signalstats) de cada corte, puxando 60% do caminho
  até a mediana das cenas de dia. Noite e telas ficam fora da correção de exposição.
- **"Ficou muito saturado"** (v1 reprovada): o tonemap com `desat=0` já entrega cor forte; somar saturação
  (até 1,12) e escurecer os médios das cenas claras (gama 0,82) adensou a cor. Aprovado: a correção nunca
  aumenta saturação (0,8–1,0) × 0,8 global e gama limitado a 0,9–1,15 — saturação média caiu de ~17,5 para ~13,5.
- **Som ambiente** a −30/−31 LUFS por corte (ganho máx. +18 dB), fala a −16 LUFS; fade de 30 ms nos cortes e
  de 8 ms na entrada da fala (senão a primeira sílaba perde o ataque).
- **Ordem cronológica** dos clipes sem nome: `com.apple.quicktime.creationdate` no ffprobe.
- **Dado na tela:** a tela da intranet mostrava um e-mail; nenhum recorte 9:16 tirava o e-mail sem cortar o
  título → opção `tela` no `edl.py`: só a faixa do título no centro, fundo = a mesma faixa desfocada.
- **Rede da nuvem:** o conector do Drive não baixa arquivo > 10 MB; liberar `drive.usercontent.google.com`
  com o link aberto. O modelo do Whisper precisa de `huggingface.co` e `*.hf.co` (com `HF_HUB_DISABLE_XET=1`).
- **v2 → v3, pedido de quem grava:** "deixa na iluminação natural dos vídeos" — a correção de cor por corte saiu
  (fica só a conversão HDR → SDR). Takes: no selfie pegar o **tchau**, não a pessoa trazendo a câmera para
  desligar; janta = **um** pedaço, comendo (pose com a mão no cabelo saiu); a fala no meio do evento era
  desnecessária; o fim mostra a tela do notebook apagando, sem recorte (a tela de login tem o e-mail da
  pessoa em letra pequena por ~2 s — avisado).
