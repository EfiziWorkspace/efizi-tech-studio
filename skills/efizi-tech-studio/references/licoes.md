# Lições — o que foi aprovado e reprovado

Feedback real de quem pediu os vídeos, versão por versão. Cada linha virou regra em outro arquivo desta skill.

## Teaser de abertura do canal (out/2026, sem gravação, 16:9)

- v1, planos de 4 s e batida entrando aos 4 s → **"muito devagar"**. v2: plano de no máximo 2,8 s, batida desde o
  quadro 0, um elemento novo a cada 1,4 s, 58 s em vez de 72. (`retencao.md`)
- Uma entrega saiu com a animação quebrada entre 36 e 39 s porque só se olhou quadros de amostra →
  **folha do vídeo inteiro a cada 0,5 s** antes de entregar. (`entrega.md`)

## Reels "Efizi → Efizi Tech, AI First" (out/2026, rosto, 9:16)

- v2: fundo inteiro trocado por um escritório de IA e close de 1,8× → **"quebrou o cenário", "zoom demais"**.
  Regra: cenário gravado fica; zoom ≤ ~1,2×; trocar só o pedaço que incomoda (o quadro branco). (`recorte-e-cenario.md`)
- Cortes **"muito secos"** → respiro de 0,1–0,3 s antes da fala; transições em cima do corte. (`takes-e-cortes.md`)
- Olhadas para o notebook (ele lia a fala) → **nenhuma** olhada pode ir ao ar; folha dos olhos a cada 0,125 s.
- Logo digital colada no quadro → reprovada; quadro "de verdade" com letra de pincel atômico, tinta falhada.
- v5 pediu: zoom leve logo depois da primeira palavra; som de "ideia" na palavra-chave; take escolhido pela
  **entonação**; a moeda (virada de assunto) vai na direção da tela e some — vai-e-volta rápido incomoda;
  explicação abstrata vira **tela cheia de motion**; metáfora falada vira cena ("ponta do iceberg" = iceberg sobe
  atrás dele); encerramento padrão no fim de todo vídeo.
- Letra preta grande em Manrope sobre laranja → **"ficou feio"**. Botão = pílula laranja com texto branco.
- Mixagem: whoosh longo e impacto grave passaram a voz → medir cada efeito que cai na fala.

## Reels da Lay — agentes de IA (out/2026, rosto + telas, 9:16)

- Blur para esconder dado na tela → **"não precisa de blur"**: usar trecho sem dado ou outra gravação.
- Biodigestor 3D desenhado à mão → **"ficou feio"**: usar o modelo 3D real do produto (do site), com a marca.
- Pausa no meio da frase → **"demorou muito"**: dividir o corte e tirar a pausa.
- Tela do sistema aparecendo antes de ela falar dele → só o avatar do agente saindo da ponta do dedo.
- Ela falando do Jira com a tela parada → **"o vídeo tem que ser interativo"**: fala em câmera, tela só quando ela
  clica. Tela de 1 s → a tela fica a explicação inteira, com zoom, zoom de volta e chicote. (`telas.md`)
- Cliques e "coin" aleatórios na parte final → **"tem que fazer sentido"**: efeito só com motivo; música tech bem
  baixa, que só se ouve nas pausas (sidechain). (`audio.md`)
- Cor → **"eu queria essa colorimetria"** (vídeo de referência de fim de tarde) → look `dourado`, medido em Lab até a
  pele bater em ±3° de matiz. (`cor.md`)
- Pegada jovem → mundo apocalíptico com robô original atrás dela no nome do agente (personagem de filme não: direito
  autoral), cérebro de pontos em "aprendem sozinhos", glitch, punch, legenda pulando. (`efeitos-e-ritmo.md`)
- A mesma animação de cérebro duas vezes → **reprovado**: a 1ª vira "problema → aprendendo → salvo".
- Círculo parado em volta do botão → **mouse andando até o botão, câmera seguindo, clique com som**.
- **"Bugou a voz… verifica essas coisas antes de me entregar"**: emenda colada na palavra anterior + voz adiantando
  até 0,13 s por brechas no áudio do concat. Agora: `verif_audio.py` (emendas, texto, sincronia) antes de toda
  entrega e áudio contínuo na montagem. (`entrega.md`, `audio.md`)

## Do processo

- Medir antes de afirmar a causa: uma suspeita ("o A-roll está com desvio") estava errada até medir corte a corte.
- Etapa interrompida deixa arquivo parcial; as etapas pulam o que existe → apagar/mover o parcial antes de rodar.
- Mostrar o plano (e a imagem gerada por IA) antes do trabalho caro; perguntar custo de crédito antes de gastar.
