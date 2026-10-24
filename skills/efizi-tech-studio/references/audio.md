# Áudio: voz, música e efeitos

A voz é a do A-roll (o vídeo da câmera). Por baixo dela vai **um** WAV (`trilha_e_efeitos.wav`) feito pelo
`montar_trilha.py`: música + efeitos. A composição toca os dois.

## A voz (o que mais importa)

- **Áudio contínuo no A-roll.** O concat de cortes deixa brechas de ~7 ms entre eles; quem lê o áudio em sequência
  (o render do HyperFrames) junta as brechas e a voz **adianta** — chegou a 0,13 s fora da boca no fim de 75 s.
  O `montar.py juntar` usa `aresample=async=1:min_hard_comp=0.001:first_pts=0` para preencher com silêncio. Conferir:
  duração do áudio do `aroll.mp4` decodificado inteiro = duração do vídeo (± 10 ms).
- Emendas sem palavra picotada: ver `takes-e-cortes.md`. Medir com `verif_audio.py`.

## Música "tech bem baixinha, só nas pausas"

- Base −14 dB e **sidechain com a voz do A-roll como chave**:
  `sidechaincompress=threshold=0.012:ratio=8:attack=25:release=300:knee=4`.
  Medido: sob a fala a música fica ~40 dB abaixo da voz (some); nas pausas aparece a −37…−45 dB.
- No encerramento (sem voz) a música sobe para −11 dB.
- Música repetida com `acrossfade=d=2` para cobrir o vídeo; fade de saída de 1,2 s.
- Música tem que ter licença de uso (gerada na sua conta, biblioteca livre). Trilha de filme/artista: não.

## Efeitos com motivo

Ficam (exemplos reais e níveis que passaram):

| Momento | Efeito | dB |
| --- | --- | --- |
| objeto 3D surgindo | `whoosh` + `sparkle` | −18 / −16 |
| avatar saindo do dedo | `ding` sintetizado | −21 |
| subida antes do cenário do vilão | trecho do pico do `riser` (2,2–3,05 s do arquivo) | −12 |
| abre o cenário | `glitch-1` (0,3 s) + `impact-bass-1` + drone sombrio | −12 / −22 / −15 |
| entrada e saída de tela | `whoosh-short` | −15 / −17 |
| clique visível na tela | `click-soft` no quadro do clique | −12 |
| problema / salvo | `error` / `chime` | −19 / −16 |
| chamada (tela divide) | `whoosh` | −18 |
| encerramento | ver `modelos/encerramento/LEIA.md` | |

Saíram (reprovados como "clique e coin aleatório"): pop em cada selo, blip em cada passo de fluxo, clique sem clique
na tela, brilho em toda frase.

- Biblioteca: `media-use/audio/assets/sfx` das skills do HyperFrames (o script procura nos lugares de instalação).
  Sintetizados (`trabalho/sfx/gera_sfx.sh`): bolha, blip, plin, ding, vento e o **drone sombrio** (ré menor grave em
  dente de serra, desafinado entre canais, sub + ruído marrom, eco).
- Efeito longo (riser 10 s, glitch 3 s) **sempre cortado**: `(tempo, nome, dB, início, duração)` no `EFEITOS`.

## Níveis (medidos, não no ouvido)

- Por janela de 0,5 s: trilha ≥ 8–10 dB abaixo da voz em toda janela com fala. Impacto grave e whoosh longo têm cauda
  de 2–3 s que passa a voz: medir a janela seguinte também.
- Integrado final: −11 a −14 LUFS, pico ≤ −1 dBFS (`ebur128=peak=true`).
- Medir com o áudio do A-roll e o WAV da trilha em mono 8 kHz e RMS por janela (numpy) — o LUFS integrado engana
  quando a música é baixa.
