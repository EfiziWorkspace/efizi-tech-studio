---
version: efizi-1
status: aprovado — canal da Efizi (Efizi Tech). Valores do design system da Efizi (30/09/2026). Para outra marca, troque este arquivo inteiro pelos tokens dela.
name: Efizi Tech — Frame
description: >
  Identidade de vídeo do canal Efizi Tech, tirada do design system da Efizi. Dois registros:
  o "universo tech" (fundo ink quase preto, linhas e luz em laranja Efizi, texto cream) e a "marca"
  (fundo cream, logo ink preta, laranja só no detalhe). Manrope em tudo que é texto; mono só para
  código. Uma cor de ênfase por quadro: o laranja.
unit: 1920×1080 (YouTube) principal; 1080×1920 (Reels/Shorts) documentado
principle: laranja é a única ênfase · mostrar a coisa real · nada inventado

colors:
  # da marca (efizi-tokens.css)
  orange: "#FF4000"        # ênfase única: linha de luz, palavra-chave, detalhe
  orange-300: "#FF9E78"    # brilho/fim de degradê de luz (só como luz, nunca como segunda cor)
  orange-700: "#B82D00"    # sombra da luz laranja
  peach: "#FE734F"         # apoio quente em ilustração, com parcimônia
  ink: "#0A0A0A"           # fundo do universo tech; texto e logo sobre cream
  cream: "#F5F3EF"         # fundo da marca; texto sobre ink
  white: "#FFFFFF"
  gray-900: "#161412"      # superfície de cartão no fundo ink
  gray-800: "#2A2723"      # borda e grade no fundo ink
  gray-600: "#6B6660"      # texto secundário sobre cream
  gray-400: "#BEB9B1"      # texto secundário sobre ink
  pulse: "#FFD500"         # SÓ selo de destaque; nunca fundo, nunca texto
  # proibidos em vídeo: teal #228474 (só link/foco de UI digital)

typography:
  # Manrope 400–800, sentence case (Google Fonts, licença OFL).
  caption:    { fontFamily: "Manrope", px169: 52, px916: 72, weight: 800, lineHeight: 1.1 }
  hook:       { fontFamily: "Manrope", px169: 84, px916: 96, weight: 800, lineHeight: 1.0, tracking: "-0.02em" }
  display:    { fontFamily: "Manrope", px169: 120, px916: 110, weight: 800, lineHeight: 0.95, tracking: "-0.03em" }
  h1:         { fontFamily: "Manrope", px169: 88, px916: 80, weight: 800, lineHeight: 1.0, tracking: "-0.02em" }
  h2:         { fontFamily: "Manrope", px169: 56, px916: 56, weight: 700, lineHeight: 1.1 }
  body:       { fontFamily: "Manrope", px169: 36, px916: 40, weight: 500, lineHeight: 1.4 }
  label:      { fontFamily: "Manrope", px169: 22, px916: 26, weight: 700, tracking: "0.08em", upper: true }
  code:       { fontFamily: "JetBrains Mono", px169: 26, px916: 30, weight: 400, lineHeight: 1.5 }
  # code: o token da marca é ui-monospace (fonte do sistema); para o render sair igual em qualquer
  # máquina usa-se a JetBrains Mono (OFL), que vem em modelos/composicao/assets/fonts/

spacing:
  margem-169: "160px laterais, 100px topo e base (área de texto x 160–1760, y 100–980)"
  margem-916: "72px laterais; respeitar zonas do Instagram (topo 220, base 440, direita 120)"
  gap: "24px"
  raio: "8px"   # --radius da marca

logo:
  preta: "assets/marca/efizi-logo-ink.svg"       # sobre cream ou branco
  branca: "assets/marca/efizi-logo-white.svg"    # sobre ink ou laranja
  cor: "assets/marca/efizi-logo-laranja.svg"
  simbolo: "assets/marca/efizi-symbol.svg"
  regra: "logo sempre do arquivo oficial, nunca redesenhado; área livre em volta de pelo menos a altura do símbolo"

components:
  legenda:
    typography: "{typography.caption}"
    color: "{colors.cream} sobre ink / {colors.ink} sobre cream; palavra ativa em {colors.orange}"
    description: "2–3 palavras (Reels) / 3–5 (longo). Uma palavra-chave por grupo em laranja."
  linha-de-luz:
    stroke: "2–4px {colors.orange}, brilho em {colors.orange-300}"
    description: "O fio condutor do universo tech: dados correndo, conexão entre agentes, traço da câmera."
  cartao:
    backgroundColor: "{colors.gray-900}"
    border: "1px solid {colors.gray-800}"
    radius: "{spacing.raio}"
    description: "Base para interface, código e número sobre ink. Sem sombra pesada."
  no-de-agente:
    shape: "círculo ou cartão pequeno {colors.gray-900} com borda {colors.orange} quando ativo"
    description: "Um agente de IA. Ativo = borda e pulso laranja; ligado aos outros por linha-de-luz."
  codigo:
    typography: "{typography.code}"
    color: "{colors.gray-400}, linha em foco em {colors.cream} com marcador {colors.orange}"
    description: "Código real e sem segredo. Em destaque só se legível; senão, como textura desfocada."
  cartela-final:
    background: "{colors.cream}"
    content: "logo preta + chamada em {typography.h2} {colors.ink}; laranja só num detalhe (ponto, traço)"
---

# Efizi Tech — Frame

## Visão geral

O canal mostra a Efizi por dentro: a tecnologia que faz o saneamento acontecer. O vídeo vive em
dois registros. O **universo tech** é escuro (ink), com linhas de luz laranja ligando código, dados,
interfaces e agentes de IA. A **marca** é clara (cream), com a logo preta e muito respiro. A
passagem de um para o outro é o momento de virada de cada vídeo.

## Regras

- O laranja `#FF4000` é a única ênfase. Pulse só em selo pequeno; teal nunca aparece em vídeo.
- Manrope em sentence case (só a primeira letra maiúscula). Nada de Title Case.
- Logo só dos arquivos oficiais; preta sobre cream, branca sobre ink.
- Sem degradê sem motivo e sem sombra pesada (regra do design system). A luz laranja pode ter
  brilho, porque é luz, não preenchimento.
- Conteúdo real em primeiro plano: interface, código e nome de agente que existem de verdade.
- Palavras proibidas na tela e na narração: nomes de fabricante, fornecedor e infraestrutura da
  empresa (sistemas internos, provedores, parceiros). Na dúvida, mostrar o papel ("o sistema de vendas"),
  não o nome.
