# Recorte da pessoa, quadro branco e cenário atrás dela

## Recorte (`montar.py recorte` + `alfa`)

- `hf remove-background corte.mov -o corte_alfa.mov` (ProRes 4444 com alfa). ~2 min por 3 s de vídeo.
- Gesto rápido com borrão de movimento faz o recorte perder o braço num quadro isolado. A etapa `alfa` conserta só
  o que é falha: quadro com cobertura < 0,93 × a **mediana dos ±6 vizinhos** recebe o alfa do vizinho bom mais perto.
  (Critério global por corte confunde gesto de braço com falha; `tmedian` come 2 quadros e desalinha a legenda.)

## Quadro branco redesenhado (`quadro.py`)

Quando só o que está escrito atrás incomoda (lousa rabiscada), troque **só aquilo** — o resto do cenário fica.

1. A superfície do quadro é ajustada por um polinômio de 2º grau nos pixels visíveis dele (a escrita velha cai como
   resíduo alto e sai da conta), com o grão da câmera por cima.
2. O desenho novo (`quadro/arte_<câmera>.png`) entra em "multiplicar", levemente desfocado como o quadro real.
3. A pessoa volta na frente pelo alfa; pixel escuro (cabelo, camisa) nunca é trocado.
4. `REGIAO` = polígono do quadro por câmera, medido no 1º quadro com grade de 100 px.

Desenho "de verdade" (aprovado): letra manuscrita (Ink Free), rabiscos, tinta falhada e um pouco apagada (filtro SVG
`feDisplacementMap` + `feTurbulence` em listras). Logo digital colada no quadro foi reprovada. Arte em HTML
(`quadro/arte.html`), rasterizada com Chrome headless (`gera_arte.sh`).

## Cenário atrás da pessoa, num trecho (`pessoa.py`)

Só em **momento-chave de 2–3 s** (o mundo do "vilão" quando ela cita o agente, a animação de "aprendem sozinhos").
O vídeo inteiro com fundo trocado foi reprovado.

1. `pessoa.py` gera a pessoa recortada em **WebM VP9 com alfa** a partir do `quadro` (ou `grade`) + `alfa`:
   - `-c:v libvpx-vp9 -pix_fmt yuva420p -auto-alt-ref 0` (sem isso o alfa some);
   - alfa **apertado 3 px** (`erosion` ×3 + `gblur` 1,5): sem isso sobra uma borda clara da parede no fundo escuro;
   - **tudo abaixo da borda da mesa continua opaco** (reta por câmera em `MESA`): senão o notebook flutua no cenário.
2. No `index.html`, dentro do `#aroll-zoom` (para herdar o empurrão do corte), depois do `#aroll`:
   cenário (`.cena`, visível só no trecho) → `<video class="clip pess" src="pessoa_x.webm" data-start=… muted>`.
   `data-start` = início do corte + quadro inicial ÷ fps (exato, senão a pessoa "pula").
3. Entrada e saída com glitch de 4–5 quadros (ver `efeitos-e-ritmo.md`) escondem a troca.
4. Testar a transparência antes: o HyperFrames 0.8.177 respeita o alfa do WebM (testado sobre fundo colorido).

Conferir em `snapshot`: borda em volta do cabelo, mesa inteira, cabeça da pessoa não tapando o elemento principal
do cenário (no mundo do robô a câmera do cenário sobe junto com ele para a cabeça do robô ficar acima da dela).
