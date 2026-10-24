"""Gera compositions/outro-efizi-tech.html: encerramento padrão do canal (2,8 s), reutilizável em todo vídeo.

A logo oficial (efizi-logo-laranja.svg, um path só do potrace) é separada nas peças que se movem:
  e  = corpo do símbolo (partes 4 e 5) · bolinhas do símbolo = partes 1 (alto à direita) e 9 (baixo à esquerda)
  letras "fizi" = f (3), i (2 ponto + 6 haste), z (7), i (0 ponto + 8 haste)
Roteiro: "efizi" entra com whoosh -> "tech" digita embaixo -> o "e" dá um pulinho -> as duas bolinhas aparecem (bolha).
Os sons ficam na trilha (montar_trilha.py), nos mesmos tempos.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
svg = (RAIZ / "composicao" / "assets" / "efizi-logo-laranja.svg").read_text(encoding="utf-8")
d = re.findall(r'<path d="([^"]+)"', svg)[0]
partes = [x.strip() for x in re.split(r"(?=M)", d) if x.strip()]
assert len(partes) == 10, len(partes)

FLIP = 'transform="translate(0,1055) scale(0.1,-0.1)"'


def grupo(gid, idx):
    paths = "".join(f'<path d="{partes[i]}"/>' for i in idx)
    return f'<g id="{gid}"><g {FLIP}>{paths}</g></g>'


letras = [("oe-f", [3]), ("oe-i1", [2, 6]), ("oe-z", [7]), ("oe-i2", [0, 8])]
svg_corpo = "\n          ".join(
    [grupo("oe-e", [4, 5]), grupo("oe-dot1", [1]), grupo("oe-dot2", [9])] + [grupo(g, i) for g, i in letras]
)

html = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <!-- Encerramento padrão Efizi Tech (gerado por trabalho/v4/gera_outro.py; não editar à mão). -->
  </head>
  <body>
    <template>
      <style>
        @font-face {{ font-family: "JetBrains Mono"; src: url("assets/fonts/JetBrainsMono-400.woff2") format("woff2"); font-weight: 400; }}
        #outro-efizi-tech {{ position: absolute; inset: 0; background-color: #0a0a0a;
          background-image: radial-gradient(#2e2a26 2.5px, transparent 2.6px); background-size: 36px 36px; }}
        #oe-wrap {{ position: absolute; left: 0; right: 0; top: 780px; display: flex; justify-content: center; }}
        #oe-lock {{ display: flex; flex-direction: column; align-items: flex-end; }}
        #oe-logo {{ display: block; width: 640px; height: 281px; overflow: visible; fill: #ff4000; }}
        #oe-tech {{ display: flex; margin-top: 18px; margin-right: -0.32em; font-family: "JetBrains Mono", monospace;
          font-size: 60px; letter-spacing: 0.32em; color: #f5f3ef; line-height: 1; }}
        #oe-tech span {{ display: inline-block; }}
      </style>
      <div id="outro-efizi-tech" data-composition-id="outro-efizi-tech" data-width="1080" data-height="1920">
        <div id="oe-wrap">
          <div id="oe-lock">
            <svg id="oe-logo" viewBox="0 0 2400 1055" aria-label="Efizi">
          {svg_corpo}
            </svg>
            <div id="oe-tech"><span>t</span><span>e</span><span>c</span><span>h</span></div>
          </div>
        </div>
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          // 0,00 efizi entra (whoosh): o "e" cresce girando de leve e as letras chegam em sequência
          tl.fromTo("#oe-e", {{ scale: 0.55, rotation: -25, opacity: 0, transformOrigin: "50% 50%" }},
            {{ scale: 1, rotation: 0, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, 0.0);
          ["#oe-f", "#oe-i1", "#oe-z", "#oe-i2"].forEach((id, k) =>
            tl.fromTo(id, {{ x: -260, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, 0.08 + k * 0.07));
          tl.set(["#oe-dot1", "#oe-dot2"], {{ scale: 0, transformOrigin: "50% 50%" }}, 0);
          // 0,65 "tech" digita embaixo
          document.querySelectorAll("#oe-tech span").forEach((s, k) =>
            tl.fromTo(s, {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, 0.65 + k * 0.08));
          // 1,20 o "e" dá um pulinho (sobe, cai, amassa ao tocar o chão e volta)
          tl.to("#oe-e", {{ y: -330, duration: 0.2, ease: "power2.out", transformOrigin: "50% 100%" }}, 1.2);
          tl.to("#oe-e", {{ y: 0, duration: 0.18, ease: "power2.in" }}, 1.4);
          tl.to("#oe-e", {{ scaleY: 0.84, scaleX: 1.08, duration: 0.07, ease: "power1.out", transformOrigin: "50% 100%" }}, 1.58);
          tl.to("#oe-e", {{ scaleY: 1, scaleX: 1, duration: 0.25, ease: "elastic.out(1, 0.45)" }}, 1.65);
          // 1,62 e 1,78 as duas bolinhas aparecem (som de bolha)
          tl.to("#oe-dot1", {{ scale: 1, duration: 0.32, ease: "back.out(3)" }}, 1.62);
          tl.to("#oe-dot2", {{ scale: 1, duration: 0.32, ease: "back.out(3)" }}, 1.78);
          tl.to({{}}, {{ duration: 0.01 }}, 2.79);
          window.__timelines = window.__timelines || {{}};
          window.__timelines["outro-efizi-tech"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
out = RAIZ / "composicao" / "compositions" / "outro-efizi-tech.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print("ok", out)
