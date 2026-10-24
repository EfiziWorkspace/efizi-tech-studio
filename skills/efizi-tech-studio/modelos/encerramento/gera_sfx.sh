#!/bin/sh
# Efeitos sintetizados no ffmpeg (sem custo, sem licença): vento gelado, bolha "ploin", blip de conexão, plin de comentário, ding de ideia.
cd "$(dirname "$0")"
A="-ar 48000 -ac 2 -c:a pcm_s16le"
# vento: ruído rosa filtrado, com rajadas (tremolo lento) e um assobio fraco que sobe e desce
ffmpeg -v error -y -f lavfi -i "anoisesrc=c=pink:d=2.6:a=0.6:seed=11" -f lavfi -i "aevalsrc='0.05*sin(2*PI*(520+180*sin(2*PI*0.7*t))*t)':d=2.6" \
  -filter_complex "[0]highpass=f=180,lowpass=f=1400,tremolo=f=0.8:d=0.55[r];[r][1]amix=inputs=2:normalize=0,afade=t=in:d=0.5,afade=t=out:st=1.9:d=0.7" $A vento.wav
# bolha: varredura de 320 a 1150 Hz em 0,14 s com queda rápida (ploin); a segunda é um tom acima
for nome in bolha:320:830 bolha2:400:1000; do
  n=${nome%%:*}; r=${nome#*:}; f0=${r%%:*}; df=${r#*:}
  ffmpeg -v error -y -f lavfi -i "aevalsrc='0.7*sin(2*PI*($f0*t+($df/0.28)*t*t))*exp(-t*22)':d=0.28" -af "afade=t=in:d=0.004" $A $n.wav
done
# blip de conexão: 1400 Hz + harmônico, 70 ms
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.5*(sin(2*PI*1400*t)+0.35*sin(2*PI*2800*t))*exp(-t*55)':d=0.09" -af "afade=t=in:d=0.003" $A blip.wav
# plin de comentário: duas notas de sino (mi6 e lá6)
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.45*(sin(2*PI*1318.5*t)+0.3*sin(2*PI*2637*t))*exp(-t*7)+0.45*(sin(2*PI*1760*(t-0.11))+0.3*sin(2*PI*3520*(t-0.11)))*exp(-(t-0.11)*6)*gte(t,0.11)':d=0.8" -af "afade=t=in:d=0.003" $A plin.wav
# ding de ideia: sino claro (sol6) com brilho
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.5*(sin(2*PI*1568*t)+0.4*sin(2*PI*3136*t)+0.15*sin(2*PI*4704*t))*exp(-t*5)':d=0.9" -af "afade=t=in:d=0.003" $A ding.wav
ls -la *.wav
