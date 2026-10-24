# Takes, cortes e emendas

O bruto vem com várias tentativas da mesma frase e conversa de bastidor ("de novo", "perfeito", "show"). O trabalho
é achar a melhor tentativa de cada frase e emendar sem que se perceba.

## Escolher o take

Na ordem de importância:

1. **Frase inteira e certa** (bate com o roteiro). Preferir um take com a frase toda a costurar dois.
2. **Entonação**: ouvir as tentativas. A última nem sempre é a melhor; a que soa natural ganha.
3. **Olhar na câmera**: quem lê a fala no notebook olha para baixo. Nenhuma olhada para o computador pode ir ao ar.
   Folha dos olhos (`trabalho/olhar_takes.py`): só a faixa do rosto, um quadro a cada 0,25 s (ou 0,125 s para a
   decisão final), 12 por linha. Piscada de uma amostra fica.
   - Olhada **depois** do último som: cortar antes dela.
   - Olhada **durante** a palavra: não cortar a fala — cobrir a imagem (tela, painel, cena) nesse trecho.
4. **A mesma câmera** entre cortes vizinhos, quando houver duas.

A "deixa" da equipe ("perfeito", "graças a Deus", "show") marca o fim do take bom.

## Onde cortar

- **Pela energia do áudio, nunca pelo fim da palavra do ASR.** Medir em janelas de 20 ms (`ffmpeg … -f s16le` +
  numpy, ou `silencedetect=noise=-35dB:d=0.08`) e pôr o corte **no vale de silêncio** entre palavras.
- **Respiro:** 0,1–0,3 s antes da primeira palavra; o fim fica colado no último som (não deixar "ar" sobrando).
- **Quadros exatos:** número de quadros = `round((out − in) × fps)`; cortar com `-frames:v` e `-t n/fps`. Cortar com
  `-t` solto e mudar o fps soma 1–2 quadros por corte e a legenda escorrega.

## Emendar dois takes (a armadilha que mais custou)

Fala contínua não tem vale entre as palavras. Se o take B é emendado **no começo de uma palavra que, nele, veio
colada à anterior** ("avisa‿e abre"), a palavra entra sem ataque e soa picotada — mesmo com o corte no lugar "certo".

Regras:
- Emendar onde **os dois takes** têm silêncio: fim de frase, vírgula com pausa.
- Se a frase do take B começa antes do ponto que você quer, use o take B **desde a pausa anterior** ("acha, | avisa e
  abre um card no Jira" com o take B inteiro a partir de "avisa"), mesmo perdendo uma palavra do roteiro.
- Abrir 1–2 quadros antes do ataque, no vale; se precisar manter a soma de quadros (para não deslocar o resto do
  vídeo), tirar os mesmos quadros do silêncio do corte vizinho.
- Pausa que sobra numa emenda (0,5–0,7 s): encher com movimento (a tela entra ali), não deixar parado.

## Pausas longas no meio do take

Pausa de 0,9 s dentro da frase ("…a cada semana, [pausa] sem ninguém treinar") reprova ("demorou muito"). Dividir o
corte em dois (`s14a`, `s14b`) tirando a pausa, e cobrir o salto com um punch-in leve (escala 1,10 → 1,14).

## Depois de montar

Retranscrever o A-roll e comparar com o roteiro (`verif_audio.py`): palavra repetida ou faltando = emenda errada.
