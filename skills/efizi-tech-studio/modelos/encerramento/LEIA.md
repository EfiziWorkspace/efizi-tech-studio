# Encerramento padrão Efizi Tech (vai no fim de todo vídeo do canal)

2,8 s, 1080x1920: "efizi" entra com whoosh, "tech" (JetBrains Mono) digita embaixo, o "e" dá um pulinho e as duas
bolinhas aparecem com som de bolha. Feito com a logo oficial separada em peças (gera_outro.py).

Como usar num projeto HyperFrames:
1. Copie `outro-efizi-tech.html` para `compositions/` e as fontes `JetBrainsMono-400.woff2` para `assets/fonts/`.
2. No index: `<div data-composition-id="outro-efizi-tech" data-composition-src="compositions/outro-efizi-tech.html"
   data-start="<fim>" data-duration="2.8" data-track-index="5" data-width="1080" data-height="1920"></div>`.
   Para 16:9, ajuste `data-width/height` e o `top` de `#oe-wrap` no gera_outro.py.
3. Sons (relativos ao início do encerramento): 0,00 whoosh-cinematic −6 dB · 0,65/0,73/0,81/0,89 key-press −16 ·
   1,20 whoosh-short −18 · 1,58 click-soft −14 · 1,62 bolha −6 · 1,78 bolha2 −6. `gera_sfx.sh` sintetiza bolha,
   blip, plin, ding e vento no ffmpeg.
