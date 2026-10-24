# Cor

Dois passos sempre separados: **LUT técnica** (põe a imagem da câmera no padrão de tela) e **look** (a cara do vídeo).
Nunca usar uma LUT "criativa" no lugar dos dois.

## 1. LUT técnica (câmera Sony em S-Log3 / S-Gamut3.Cine)

`cor/gera_lut.py` calcula a `.cube` pelas fórmulas publicadas da Sony e da ITU (S-Log3 → linear → matriz
S-Gamut3.Cine→Rec.709 → ombro suave → gama 2,4). Sem arquivo baixado de terceiros.

Na cadeia do ffmpeg (o `montar.py` já faz):

```
scale=1080:1920:in_color_matrix=bt709:in_range=tv:out_range=pc,format=gbrp16le,
lut3d=file=cor/slog3cine_to_rec709.cube:interp=tetrahedral,<look>,format=yuv422p10le
```

- Entrada com `in_range=tv` (código 64–940 em 10 bits) — a LUT espera isso.
- Conferir por número: preto esmagado e alta estourada em % de pixels, não no olho.
- Celular ou câmera sem log: pular a LUT, só o look.

## 2. Looks (`cor/looks.py`)

Cada look é uma cadeia de filtros do ffmpeg depois da LUT. Os três que existem:

| Look | Cara | Uso |
| --- | --- | --- |
| `efizi` | quente leve, contraste 1,10, saturação 1,16 | padrão de escritório |
| `tech` | sombra fria, contraste 1,15 | trecho "tecnológico", troca escondida atrás de transição |
| `dourado` | fim de tarde: preto levemente levantado, altas que caem suave, médios e altas puxados para o dourado, saturação 1,17 + vibrance 0,18, nitidez leve | o preferido para Reels — veio de uma referência pedida |

O `dourado`:

```
curves=all='0/0.03 0.25/0.235 0.5/0.52 0.8/0.84 1/0.975',
colorbalance=rs=0.02:gs=0.0:bs=-0.04:rm=0.02:gm=0.012:bm=-0.06:rh=0.07:gh=0.015:bh=-0.04,
eq=saturation=1.17:gamma=1.02,vibrance=intensity=0.18,unsharp=5:5:0.35:5:5:0
```

Corte em que a câmera filma um monitor fica no look neutro (senão a tela amarela).

## 3. Copiar a cor de uma referência ("eu queria essa colorimetria")

Medir, não chutar:

1. Salvar um quadro da referência (print serve) em `referencia/cor/`.
2. `python cor/medir.py ref.png x0 y0 x1 y1` — luma L* (p2/p50/p98), saturação, tinta (a*, b*) de sombras/médios/altas
   e a pele (caixa na testa/bochecha, longe de barba e óculos): L*, croma e **matiz**.
3. `python cor/testar_look.py <look> <clipe> <tempo> <cx> <y0>` aplica o look num quadro do bruto pelo mesmo caminho
   do `montar.grade`; medir de novo e comparar.
4. Ajustar e repetir até: **matiz da pele a ±3°** da referência, b* dos médios na mesma faixa, preto no mesmo nível.
   Não copiar a luma da pele (cada pessoa e luz é uma), nem a saturação média de uma cena com mato (o cenário muda).
5. Comparar lado a lado em 3 câmeras/cenas diferentes antes de regradear tudo.

Armadilhas medidas:
- `rm` (vermelho nos médios) alto deixa a pele rosada → baixar `rm` e subir um pouco `gm`.
- Altas puxadas para o amarelo deixam o quadro branco "sujo" → altas mais para o vermelho (`rh`), menos verde (`gh`).
- Cor em pipe para o Python: dizer `in_color_matrix=bt709` na leitura e `out_color_matrix=bt709` na volta, senão o
  swscale usa BT.601 e a cor muda.
- Concat de ProRes perde primárias/transferência no H.264: gravar
  `-bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`.

## 4. Trocar o look de um vídeo pronto

Mudar `look` no `edl.json`, mover `cortes/grade`, `cortes/quadro` e `cortes/tela` para `cortes/antigo_<look>/` e rodar
`grade → quadro → tela → juntar` (o recorte não precisa refazer). Os recortes de pessoa (`pessoa.py`) também.
