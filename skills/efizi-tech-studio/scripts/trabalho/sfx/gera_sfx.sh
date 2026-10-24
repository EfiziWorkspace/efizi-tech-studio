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
# drone do mundo apocalíptico (Ultron): ré menor grave em "dente de serra" (6 harmônicos), um pouco desafinado entre
# os canais, sub em ré1 e ronco de ruído marrom; entra com o impacto e some em 0,6 s no glitch de saída
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.07*(sin(2*PI*73.42*t)+sin(2*PI*146.84*t)/2+sin(2*PI*220.26*t)/3+sin(2*PI*293.68*t)/4+sin(2*PI*367.1*t)/5+sin(2*PI*440.52*t)/6 + sin(2*PI*87.61*t)+sin(2*PI*175.22*t)/2+sin(2*PI*262.83*t)/3+sin(2*PI*350.44*t)/4 + sin(2*PI*110.3*t)+sin(2*PI*220.6*t)/2+sin(2*PI*330.9*t)/3+sin(2*PI*441.2*t)/4) + 0.16*sin(2*PI*36.71*t)|0.07*(sin(2*PI*73.0*t)+sin(2*PI*146.0*t)/2+sin(2*PI*219.0*t)/3+sin(2*PI*292.0*t)/4+sin(2*PI*365.0*t)/5+sin(2*PI*438.0*t)/6 + sin(2*PI*87.0*t)+sin(2*PI*174.0*t)/2+sin(2*PI*261.0*t)/3+sin(2*PI*348.0*t)/4 + sin(2*PI*109.7*t)+sin(2*PI*219.4*t)/2+sin(2*PI*329.1*t)/3+sin(2*PI*438.8*t)/4) + 0.16*sin(2*PI*36.71*t)':d=3.3:c=stereo" \
  -f lavfi -i "anoisesrc=c=brown:d=3.3:a=0.5:seed=5" \
  -filter_complex "[0]tremolo=f=3.2:d=0.25,lowpass=f=1100[a];[1]lowpass=f=180,aformat=channel_layouts=stereo[n];[a][n]amix=inputs=2:normalize=0,aecho=0.8:0.6:120|260:0.35|0.22,afade=t=in:d=0.12,afade=t=out:st=2.7:d=0.6" $A drone_apoc.wav
