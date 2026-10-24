# Formatos e medidas

## Saídas

| Formato | Resolução | fps | Duração | Observação |
| --- | --- | --- | --- | --- |
| Reels (Instagram) | 1080×1920 (9:16) | 30 | ideal 20–60 s | o mesmo arquivo serve para Shorts e TikTok |
| Shorts (YouTube) | 1080×1920 (9:16) | 30 | ideal 20–60 s | |
| YouTube longo | 1920×1080 (16:9) | 30 (ou o da gravação) | o que o assunto pedir | capítulos a cada bloco |

Codificação de entrega: MP4, vídeo H.264, áudio AAC 48 kHz. Confira com `ffprobe` depois do render.

Os limites de duração das plataformas mudam com frequência; confira na própria plataforma antes de
publicar algo acima de 90 s.

## Zonas seguras do Reels (1080×1920)

O Instagram desenha por cima do vídeo. Texto, legenda e rosto ficam **fora** dessas faixas:

```
┌──────────────────────────┐  0
│   topo: ~220 px livre     │  nome da conta, "Reels"
├──────────────────────────┤  220
│                     │ ~  │
│   ÁREA SEGURA       │120 │  coluna da direita: curtir,
│   texto e legenda   │ px │  comentar, compartilhar
│   ficam aqui        │    │
│                     │    │
├──────────────────────────┤  ~1480
│   base: ~440 px livre     │  legenda do post, @, música
└──────────────────────────┘  1920
```

- Legenda do vídeo: entre 62% e 68% da altura (≈1190–1300 px), centralizada, largura máxima ~860 px.
- Texto do gancho: na metade de cima da área segura (≈300–800 px).
- Nada importante nos 120 px da direita.

## Do mesmo bruto para os dois formatos

Grave em 16:9 com a pessoa no centro e espaço em volta, ou em 9:16 direto se o vídeo for só curto.
Do 16:9 para o 9:16:
- Recorte centralizado na pessoa (reframe), sem esticar.
- Visuais (prints, código) entram ocupando a metade de cima da tela, com a pessoa embaixo, ou em
  tela cheia por poucos segundos.
- Refaça a legenda no tamanho do 9:16; não reaproveite a do 16:9.
