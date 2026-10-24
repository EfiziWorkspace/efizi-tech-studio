# Conferência antes de entregar

Nada sai sem passar por aqui. Dois defeitos já chegaram a quem pediu porque a conferência só olhava imagem: uma
emenda com voz picotada e a voz adiantando em relação à boca. Desde então a voz é medida.

## 1. Imagem

- `ffprobe`: duração, 1080×1920, 23,976 fps, áudio AAC 48 kHz.
- **Folha do vídeo inteiro**, um quadro a cada 0,5 s: `ffmpeg -i v.mp4 -vf "fps=2,scale=216:-1,tile=10x15" -frames:v 1 folha.jpg`.
  Olhar tudo: cena faltando, título preso na tela, elemento aparecendo fora de hora (`immediateRender`), borda do
  recorte, texto em zona do Instagram.
- `snapshot` com zoom nos detalhes (card, avatar, cursor): `hf snapshot --at 6.6 --zoom "#ultron" --zoom-scale 2`.

## 2. Voz — `python trabalho/verif_audio.py ../saida/video.mp4`

1. **Emendas:** energia da voz 40 ms antes e depois de cada corte. Acima de −32 dB = voz colada no corte → abrir o
   bruto nesse ponto e ver se é palavra cortada (corrigir) ou respiração/ruído da sala (aceitar, anotando).
2. **Texto:** retranscreve o vídeo e compara corte a corte com o `texto` do EDL. Palavra repetida ou faltando =
   emenda errada. Nome próprio trocado ("efise", "gira") é o ASR — conferir à mão.
3. **Sincronia voz × boca:** correlação do áudio do vídeo final com o bruto de cada corte. Tem que dar 0 ms em todos;
   acima de 40 ms = fora (ver `audio.md`, áudio contínuo).

## 3. Som

- `ffmpeg -i v.mp4 -af ebur128=peak=true -f null -` → −11 a −14 LUFS, pico ≤ −1 dBFS.
- Trilha × voz por janela (`audio.md`): nenhum efeito acima da voz.

## 4. Antes de mandar

- Guardar a anterior: `saida/video-vN.mp4`.
- Mensagem de entrega: o que mudou, o que foi conferido (com os números) e o que ficou de fora ou não foi conferido.
- Créditos de IA gastos, se houve.
