---
name: efizi-tech-studio
description: >
  Estúdio de edição de vídeo da Efizi Tech para o Claude Code: transforma gravação bruta (câmera, celular, gravação
  de tela) em Reels, Shorts ou YouTube com gancho, legenda palavra por palavra, cor de cinema, telas com zoom e
  chicote, cenário atrás da pessoa, efeitos com motivo, música que abaixa sozinha na fala e conferência de voz antes
  de entregar. Usa o HyperFrames (HTML -> MP4). Use SEMPRE que o pedido for editar, cortar, legendar, montar, colorir,
  "deixar dinâmico", "pegada jovem", criar gancho, fazer Reels/Shorts, escolher takes, tirar silêncio, pôr música ou
  efeito, gerar cena com IA (Kairogen) ou revisar um vídeo — mesmo que a pessoa não diga "skill" nem "edição".
---

# Efizi Tech Studio — edição universal

Esta skill é o jeito de editar que a Efizi Tech construiu em vários vídeos reais, escrito como processo. Ela decide
**o que** o vídeo precisa ter para prender e **com que cara**; o HyperFrames faz o **como** (transcrever, compor em
HTML, renderizar MP4). Tudo aqui foi medido em vídeo de verdade e passou pela aprovação (ou reprovação) de quem pediu
— as lições estão em `references/licoes.md`.

## As quatro promessas

Todo vídeo que sai daqui cumpre as quatro. Se uma falhar, o vídeo não está pronto.

1. **Gancho nos 3 primeiros segundos** — visual, falado e escrito desde o quadro 0. → `references/ganchos.md`
2. **Falou, mostrou** — citou uma coisa concreta (sistema, número, site, erro), ela aparece na tela no mesmo instante,
   e a tela fica enquanto a pessoa explica. Nada parado por mais de 3 s no Reels. → `references/retencao.md`,
   `references/telas.md`
3. **Legenda sempre**, palavra por palavra, a palavra dita "pulando". → `references/legendas.md`
4. **Voz perfeita** — nenhuma palavra picotada nas emendas, voz sincronizada com a boca, música e efeitos abaixo da
   fala. Conferido por número antes de entregar. → `references/audio.md`, `references/entrega.md`

## Antes de começar

- **Ferramentas** (uma vez por máquina): ver o `README.md` do repositório — Node 22+, FFmpeg, Python 3.11+ com
  `numpy` e `pillow`, as skills do HyperFrames (`npx hyperframes skills update`) e o modelo de transcrição
  (`npx hyperframes models install parakeet`).
- **Identidade visual:** `modelos/frame.md` é a da Efizi Tech (preto com pontos, laranja `#FF4000`, Manrope, "tech" em
  JetBrains Mono). Para outra marca, troque o `frame.md` pelos tokens dela — o resto da skill não muda.
  → `references/marca-efizi-tech.md`
- **Formato:** decida antes de tudo se é A (rosto + prova), B (explicativo sem rosto) ou C (bastidor curto).
  → `references/modelos.md`, medidas e zonas seguras em `references/formatos.md`.
- **Pergunte, não invente:** nome do canal, @, chamada final, número, nome de sistema. Se não sabe, pergunte a quem
  pediu o vídeo. Número sem fonte não entra.

## Onde ficam as coisas

```
<pasta de trabalho>/
├── hyperframes/                 (opcional) clone do HyperFrames, se quiser ler as skills de lá
└── videos/<AAAA-MM-DD>-<assunto>/   criado por scripts/novo_projeto.py
    ├── brutos/                  gravação original — nunca alterar (câmera, celular, telas/)
    ├── referencia/              vídeo de referência, prints, fotos de produto
    ├── cor/                     LUT técnica (gera_lut.py), looks.py, medir.py, testar_look.py
    ├── trabalho/                edl.json, scripts da montagem, cortes/, transcr/, verif/
    ├── composicao/              projeto HyperFrames: index.html, assets/, compositions/
    └── saida/                   MP4 entregue (as versões anteriores ficam com -v2, -v3…)
```

Crie um projeto novo com:

```bash
python <skill>/scripts/novo_projeto.py videos/2026-10-24-meu-video
```

## Fluxo de um vídeo (resumo — o detalhe está em `references/fluxo.md`)

Mostre o plano nos dois pontos ✋ e espere o ok: mudar o plano custa segundos, mudar depois do render custa minutos.

1. **Receber o bruto** em `brutos/`; `ffprobe` (duração, fps, rotação, perfil de cor — câmera Sony grava S-Log3).
2. **Transcrever em português** (`--engine parakeet --language pt`); o ASR erra nomes próprios: corrigir na legenda.
3. **Escolher os takes** — pela fala inteira, pela entonação e pelo olhar (folha dos olhos a cada 0,125–0,25 s);
   cortar no silêncio medido com `silencedetect`/energia, nunca pelo fim de palavra do ASR. → `references/takes-e-cortes.md`
4. **✋ Roteiro de retenção** (`ROTEIRO.md`): gancho escolhido entre 3, tabela falou-mostrou (tempo · fala · tela · som),
   onde entra tela gravada, cenário, efeito. → `references/retencao.md`, `references/efeitos-e-ritmo.md`
5. **Montar o A-roll** com `trabalho/montar.py` (grade → recorte → alfa → quadro → tela → juntar): cortes em quadros
   exatos, cor técnica + look, A-roll H.264 com áudio contínuo. → `references/cor.md`, `references/recorte-e-cenario.md`
6. **Compor** no `composicao/index.html` (ler `hyperframes-core` antes de escrever HTML de composição): legendas,
   telas, selos, cenas, 3D, glitch, CTA, encerramento. Exemplo completo em `exemplos/reels-agentes/`.
7. **Trilha** com `trabalho/montar_trilha.py`: música baixa com sidechain na voz + efeitos com motivo. → `references/audio.md`
8. **✋ Revisão**: `hyperframes lint`, `check` e `snapshot --at …` nos momentos-chave; olhar os quadros.
9. **Renderizar** (`render --fps 24000/1001 --quality delivery --no-best-effort`) e **conferir antes de entregar**:
   folha a cada 0,5 s, LUFS, `trabalho/verif_audio.py` (emendas, texto, sincronia). → `references/entrega.md`
10. **Entregar** com o que mudou, o que foi conferido e o que ficou de fora. Guardar a versão anterior como `-vN`.

## Mapa das referências

| Assunto | Arquivo |
| --- | --- |
| Passo a passo com comandos | `references/fluxo.md` |
| Escolher take, cortar, emendar, olhar | `references/takes-e-cortes.md` |
| Cor: LUT S-Log3, looks, copiar a cor de uma referência | `references/cor.md` |
| Recorte da pessoa, quadro branco redesenhado, cenário atrás dela | `references/recorte-e-cenario.md` |
| Gravação de tela: chicote, zoom, mouse andando, câmera seguindo | `references/telas.md` |
| Pegada jovem: punch, glitch, legenda pulando, 3D no dedo, cérebro, selos, CTA | `references/efeitos-e-ritmo.md` |
| Música, sidechain, efeitos sonoros, níveis | `references/audio.md` |
| Cena e imagem com IA na Kairogen (modelos, custo, armadilhas) | `references/kairogen.md` |
| Conferência antes de entregar | `references/entrega.md` |
| O que foi aprovado e reprovado, versão por versão | `references/licoes.md` |
| Ganchos, retenção, legendas, formatos, modelos, checklist | `references/*.md` |
| Identidade Efizi Tech e encerramento padrão | `references/marca-efizi-tech.md`, `modelos/` |

## Regras que nunca mudam

- **O cenário gravado fica.** Não trocar o fundo inteiro nem dar zoom forte (máx. ~1,2× no rosto). Cenário atrás da
  pessoa só em momento-chave de 2–3 s, entrando e saindo com transição. Mexer só no pedaço que incomoda.
- **Tela só quando a pessoa mexe ou explica aquilo**, e fica a explicação inteira. Tela parada com a pessoa falando
  de outra coisa reprova; insert de 1 s também.
- **Efeito sonoro tem que ter motivo** (revelação, transição de tela, clique visível, chamada). Pop em cada selo
  vira barulho.
- **Nada de personagem, logo ou música de filme/marca de terceiros** (direito autoral). Cena "no clima de" um filme
  é feita com design original.
- **Nada inventado:** número, funcionalidade, resultado e nome de sistema têm que existir. Dado sensível (e-mail,
  cliente, valor interno) não aparece na tela — cortar o trecho ou trocar a gravação.
- **Crédito de IA custa dinheiro:** estimar e pedir o ok antes de gerar (`references/kairogen.md`).
- **Conferir antes de entregar**, sempre por número: emendas, sincronia, LUFS, quadros. "Parece bom" não é conferência.
- **Uma cor de ênfase por quadro.** Se tudo é destaque, nada é.

## O que não fazer

- Abrir com "Fala, galera", "Nesse vídeo eu vou…", logo ou vinheta antes do gancho.
- Deixar a pessoa falando sem nada mudar na tela por mais de 3 s no Reels.
- Pôr texto nas zonas onde o Instagram desenha botões (topo 220 px, base 440 px, direita 120 px no 1080×1920).
- Cortar no meio de palavra, emendar take colado na palavra anterior ou entregar sem ouvir/medir as emendas.
- Rodar etapa de novo em cima de arquivo parcial de execução interrompida (as etapas pulam o que existe).
