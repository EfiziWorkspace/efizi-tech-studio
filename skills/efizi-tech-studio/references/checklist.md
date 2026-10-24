# Checklist antes do render

Passe item por item olhando os quadros de amostra do preview. Item que falhou volta para a
composição; só renderize com tudo marcado.

## Gancho
- [ ] O quadro 0 já tem algo concreto em movimento (não é fundo vazio, logo nem rosto parado).
- [ ] O texto do gancho está na tela desde o quadro 0, legível sem som, em até 7 palavras.
- [ ] A promessa é dita antes de 3 s.
- [ ] Não há "fala, galera", apresentação nem vinheta antes do gancho.

## Retenção
- [ ] Toda coisa concreta citada aparece na tela quando é dita (confira contra a tabela do `ROTEIRO.md`).
- [ ] Nenhum trecho com só o rosto por mais de 3 s (Reels) ou 5 s (longo).
- [ ] Os visuais são da coisa real (print, logo, número com fonte), não genéricos.
- [ ] Os tipos de visual se alternam; não há três iguais seguidos.
- [ ] Vídeo longo: há re-gancho a cada 45–60 s.

## Legenda
- [ ] Transcrita com `--language pt` (não traduzida para inglês).
- [ ] Termos técnicos corrigidos pelo glossário.
- [ ] Legenda presente do começo ao fim, sincronizada com a fala.
- [ ] Nenhum grupo dura menos de 0,5 s.
- [ ] Legenda nunca fica atrás de um cartão ou print.

## Identidade
- [ ] Cores e fontes só do `frame.md`.
- [ ] Uma cor de ênfase por quadro.
- [ ] Reels: nada importante nas zonas do Instagram (topo 220 px, base 440 px, direita 120 px).

## Som
- [ ] A voz está sempre acima da música e dos efeitos.
- [ ] Não há corte de áudio no meio de palavra.
- [ ] Efeitos sonoros marcam as trocas de visual, sem exagero.

## Entrega
- [ ] **O MP4 final visto inteiro, um quadro a cada 0,5 s** (`ffmpeg -vf "fps=2,scale=320:-1,tile=6x6"`), e não só
      os quadros de amostra do preview. A v2 do teaser Efizi Tech foi entregue com a formação do cérebro quebrada
      entre 36 e 39 s, e a amostra pulou exatamente esse trecho.
- [ ] Resolução, fps e duração conferidos com `ffprobe`.
- [ ] Reels termina no auge (ou em loop); longo termina com chamada e próximo vídeo.
