"""Looks criativos aplicados DEPOIS da conversão técnica S-Log3 -> Rec.709 (que fica em slog3cine_to_rec709.cube).

Os dois looks partem do mesmo Rec.709 técnico e só mexem em contraste, saturação e balanço de cor por faixa
(sombras / meios / luzes). A pele fica protegida porque a saturação sobe pouco e o calor vai para as luzes.
  efizi : vivo e quente, puxando para o laranja da marca (#FF4000) nas luzes.
  tech  : mais contraste, sombras levemente frias (grafite), luzes ainda quentes — acompanha o fundo escuro.
"""

LOOKS = {
    "efizi": (
        "eq=contrast=1.10:brightness=0.01:saturation=1.16:gamma=0.98,"
        "colorbalance=rs=0.015:gs=0.0:bs=-0.02:rm=0.02:gm=0.0:bm=-0.02:rh=0.035:gh=0.01:bh=-0.035,"
        "vibrance=intensity=0.10"
    ),
    "tech": (
        "eq=contrast=1.15:brightness=-0.005:saturation=1.08:gamma=0.97,"
        "colorbalance=rs=-0.025:gs=0.0:bs=0.035:rm=0.0:gm=0.0:bm=0.0:rh=0.03:gh=0.005:bh=-0.03,"
        "vibrance=intensity=0.06"
    ),
    # "dourado": a cor do vídeo de referência pedido (youtu.be/pUPK1pHW6MU, fim de tarde): preto levemente
    # levantado, altas que caem suave, tudo puxado para o dourado e bem saturado, pele quente.
    "dourado": (
        "curves=all='0/0.03 0.25/0.235 0.5/0.52 0.8/0.84 1/0.975',"
        "colorbalance=rs=0.02:gs=0.0:bs=-0.04:rm=0.02:gm=0.012:bm=-0.06:rh=0.07:gh=0.015:bh=-0.04,"
        "eq=saturation=1.17:gamma=1.02,"
        "vibrance=intensity=0.18,unsharp=5:5:0.35:5:5:0"
    ),
}
