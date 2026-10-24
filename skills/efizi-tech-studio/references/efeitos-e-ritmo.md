# Efeitos e ritmo — a pegada jovem

Tudo aqui está implementado em `exemplos/reels-agentes/index_modelo.html` (GSAP numa timeline pausada, como o
HyperFrames pede). Use como peças: copie a função e ajuste os tempos às palavras da legenda.

## Gancho (0–5 s)

- **Zoom leve logo depois da primeira palavra** (1,0 → 1,07 em 0,7 s) e empurrão lento até o fim da frase.
- **Objeto saindo da ponta do dedo** quando ela aponta: biodigestor 3D girando (Three.js + modelo `.glb` do site,
  `GLTFLoader` com `MeshoptDecoder` se o arquivo for comprimido; sem o decoder o corpo some), surge com `back.out`
  no dedo, gira rápido e desacelera mostrando a marca de frente, sobe e some.
- Título do gancho numa caixa escura (laranja sobre fundo claro reprova contraste).

## Legenda que pula

Grupos de até 3 palavras / 20 caracteres, na faixa de 1300 px (fora das zonas do Instagram). Cada palavra entra a
0,55 de opacidade e, quando é dita, **pula**: escala 1 → 1,22 em 0,07 s e assenta com mola (`back.out(2.6)`, 0,24 s).
Palavra com `*` no `v_palavras.js` fica laranja (uma por grupo).

## Punch nas palavras-chave

`punch(t)`: o `#aroll-wrap` vai a 1,07 e volta em 0,42 s (`power3.out`), origem em 50% 35% (rosto). Em "IA", no nome
do agente (1,1 + tremida), "sozinhos", "Jira", "PR", "AI First". Não em toda frase — vira tique.

## Glitch nas viradas de cena

`glitch(t, n)`: 4–5 quadros com faixas horizontais coloridas em `mix-blend-mode: difference` (laranja, ciano, branco,
posições sorteadas com semente fixa), filtro SVG de separação RGB (`feColorMatrix` + `feOffset` ±16 px) e tremida em x.
Usar só para entrar/sair de cenário, de tela especial e em virada de assunto. Som: `glitch-*` cortado em 0,2–0,25 s.

## Cenário de "vilão" quando ela cita o agente

Ex.: "Esse aqui é o Ultron" → mundo apocalíptico original atrás dela por 3 s: cidade em ruínas, céu vermelho, robô
gigante de olhos vermelhos (Kairogen — ver `kairogen.md`), brasas passando na frente dela (canvas 2D com semente),
relâmpago (flash vermelho em `screen`), tremida na revelação, card do agente (avatar + nome + papel + "no ar")
saindo da ponta do dedo. Entrada e saída com glitch. Ver `recorte-e-cenario.md` para pôr o cenário atrás dela.

## "Eles aprendem sozinhos" — duas animações diferentes

A mesma animação duas vezes no vídeo reprovou. Variar:

1. **Problema → aprendendo → salvo** (1ª vez): acima da cabeça dela, em fundo preto com pontos: triângulo de alerta
   laranja com tremida + "problema detectado" → anel de carregamento enchendo + barra + "aprendendo…" → ícone de
   salvar com check + "aprendizado salvo" no instante da palavra-chave. Som: `error` no problema, `chime` no salvo.
2. **Cérebro de pontos** (2ª vez): Three.js, 1300 pontos em dois hemisférios com sulcos, nascendo da frente para trás,
   cada um ligando 3 vizinhos (até 0,26), branco ao nascer e esfriando para laranja; cor aditiva satura para amarelo —
   usar laranja escuro `[0.85, 0.16, 0]` e linhas a 0,4.

## Selos, fluxos e gráfico

- **Selo** (pílula laranja ou contornada) com a palavra que ela diz, no instante da palavra ("varre o código",
  "card no Jira", "+ alerta pra gente"). O texto do selo tem que ser o que ela fala — selo com palavra que ela não diz
  ("vulnerabilidade" quando ela diz "problemas") confunde.
- **Fluxo** em passos (`card → correção → PR aberto`) entrando um a um na fala.
- **Gráfico** de linha subindo em "fica mais inteligente a cada semana", sem número inventado ("semana a semana").

## Chamada e encerramento

- Chamada: a tela divide — painel de cima com a assinatura Efizi Tech e o botão "+ Siga a Efizi Tech" (pílula
  laranja, texto branco), a pessoa na metade de baixo; costura laranja entre os dois.
- Esmaece para o **encerramento padrão** (`modelos/encerramento/`, 2,8 s): "efizi" entra com whoosh, "tech" digita
  embaixo, o "e" pula e as bolinhas aparecem com som de bolha.

## Ritmo

Algo muda na tela a cada 1,5–3 s no Reels. Alternar tipos (câmera → tela → selo → cena → câmera com punch); três
coisas iguais seguidas cansam igual a nada mudando.
