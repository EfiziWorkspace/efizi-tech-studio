# Telas (gravação de tela)

## Quando a tela entra

- **Só quando a pessoa mexe ou explica aquilo.** Falar do sistema com a tela parada atrás reprovou ("o vídeo tem que
  ser interativo"): a fala fica em câmera e a tela entra na palavra em que ela clica/aponta.
- **Fica a explicação inteira.** Insert de 1 s reprovou. Ex.: "Dá uma olhada nisso aqui" → a tela fica até ela
  terminar de explicar (6 s), com gráfico por cima no fim.
- Ela aponta para algo que ainda não apareceu ("Esse aqui é o …")? O objeto nasce **na ponta do dedo** (avatar,
  produto 3D) — sem tela de sistema antes da hora.

## Gravação > câmera filmando o monitor

Pedir a gravação real (OBS, gravação do Chrome). `trabalho/telas.py`:
- corta a barra do navegador (88 px em 1280×720: abas e endereço não aparecem — nem URL nem outras abas);
- sobe para 1920 de largura com lanczos (o zoom chega a 2×);
- junta trechos: pular carregamento (ex.: card do Jira levou 3 s para abrir — cortar do clique para o card aberto);
- grava a 24000/1001, sem áudio (a voz é a do A-roll).

Tirar da tela antes: e-mail, nome de cliente, valor interno. Se não der para cortar, escolher outro trecho.

## A animação `tela()` (no `index.html` do exemplo)

1. **Chicote de entrada**: a tela vem da direita (x 1080 → 0, `skewX` −7 → 0, 0,38 s `expo.out`) empurrando a
   pessoa para a esquerda (−380 px). Começar um pouco antes do corte de câmera esconde o salto.
2. **Zoom no que ela cita**: escala 1,3–2,0 mirando um ponto em pixels da gravação (`[t, px, py, escala, duração]`);
   a janela é presa nas bordas (sem mostrar fundo de lado).
3. **Zoom de volta** quando ela termina de falar daquilo.
4. **Chicote de saída**: a tela vai para a esquerda (`expo.in`, 0,3 s) e a pessoa volta da direita.
5. Rótulo pequeno em cima da janela (nome + mono laranja: "Agentes · Tech Hub").
6. Som: whoosh curto só na entrada e na saída.

## Mouse andando e câmera seguindo (o "é só clicar aqui")

Círculo parado em volta do botão reprovou. O que funcionou:
- Achar onde o cursor da gravação **para** (caixa dos pixels claros num quadro) e esconder o cursor real com um
  **remendo da cor do fundo** daquele ponto em diante.
- Um cursor desenhado (SVG de seta, branco com contorno preto) **parte do mesmo ponto** e anda até o botão, com x e y
  em curvas diferentes (`power3.inOut` no x, `power2.out` no y = arco de mão de verdade).
- A **câmera segue o mouse**: zoom 1,8 no ponto de partida e o mesmo tempo/curva até o botão.
- No clique: o cursor "aperta" (escala 0,8 e volta), o botão acende (branco em `screen`), um anel laranja se abre e
  o som de clique cai **no quadro do clique**.
- `fromTo` de algo que deve aparecer só depois precisa de `immediateRender: false` — senão aparece desde o começo
  (foi o "círculo parado").

## Clique real da gravação

Se a gravação já tem o clique (abrir o card), sincronizar: o quadro do clique na gravação cai na palavra da fala
("Olha esse card aqui…"), ajustando o início do trecho.
