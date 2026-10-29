# Lista de cortes (arquivo, entrada s, saída s, opções). Ordem obrigatória:
# abertura rápida (TEASER, ~1,5 s por cena) → ida1..ida6 → evento1..6 → aleatórios manhã (+ ev) → almoço → aleatórios tarde → janta → volta → volta2
TEASER = [  # cenas do evento passando rápido antes da ida (versões novas, exportadas pela pessoa)
  ("IMG_3478.MOV", 0.5, 2.0, {}), ("novo_IMG_3444.MOV", 10.5, 12.0, {}), ("novo_IMG_3447.MOV", 3.0, 4.5, {}),
  ("novo_IMG_3474.MOV", 4.0, 5.5, {}), ("novo_painel_37a4ecb5.mov", 1.5, 3.0, {"girar": "transpose=2", "cx": 0.46}),
  ("novo_IMG_3491.MOV", 6.0, 7.5, {}), ("IMG_3461.MOV", 3.8, 5.3, {}),
]
V1 = [  # narrada (~65 s)
  ("ida1.MOV", 2.6, 5.0, {}), ("ida2.MOV", 0.0, 2.2, {}), ("ida3.MOV", 3.8, 6.2, {}),
  ("ida4a.MOV", 3.0, 5.6, {}), ("ida4b.MOV", 9.8, 12.0, {}),
  ("ida5.mov", 30.0, 32.5, {}), ("ida5.mov", 66.5, 68.5, {}), ("ida6.MOV", 3.5, 5.8, {}),
  ("evento1.MOV", 2.5, 5.5, {}), ("evento2.MOV", 0.3, 2.8, {}), ("evento3.MOV", 2.6, 5.0, {}),
  ("evento4.mov", 45.0, 47.0, {}), ("evento5.MOV", 5.4, 8.2, {}), ("evento6.MOV", 9.0, 11.2, {}),
  ("IMG_3444.MOV", 8.0, 10.8, {}), ("IMG_3464.MOV", 2.8, 5.3, {}), ("ev.MOV", 19.5, 21.8, {}),
  ("IMG_3461.MOV", 3.0, 6.5, {}), ("IMG_3478.MOV", 0.3, 2.8, {}), ("novo_IMG_3474.MOV", 1.8, 4.4, {}), ("IMG_3475.MOV", 2.4, 4.6, {}),
  ("almoco.MOV", 0.0, 2.8, {}),
  ("novo_painel_37a4ecb5.mov", 0.5, 3.0, {"girar": "transpose=2", "cx": 0.46}), ("IMG_3480.MOV", 1.2, 4.2, {}), ("IMG_3493.MOV", 6.0, 8.8, {}),
  ("janta.MOV", 7.0, 10.0, {}),
  ("volta1.MOV", 4.3, 7.0, {}), ("volta2.MOV", 7.6, 11.4, {}),
]
V2 = [  # só música (~50 s)
  ("ida1.MOV", 2.8, 4.6, {}), ("ida2.MOV", 0.2, 1.8, {}), ("ida3.MOV", 4.2, 6.0, {}),
  ("ida4a.MOV", 3.0, 5.2, {}), ("ida4b.MOV", 10.0, 11.8, {}),
  ("ida5.mov", 30.5, 32.5, {}), ("ida6.MOV", 3.8, 5.6, {}),
  ("evento1.MOV", 3.0, 5.4, {}), ("evento2.MOV", 0.5, 2.5, {}), ("evento3.MOV", 2.9, 4.8, {}),
  ("evento4.mov", 45.2, 46.8, {}), ("evento5.MOV", 5.6, 7.8, {}), ("evento6.MOV", 9.3, 11.1, {}),
  ("IMG_3444.MOV", 8.2, 10.4, {}), ("IMG_3464.MOV", 3.0, 4.8, {}), ("ev.MOV", 19.8, 21.6, {}),
  ("IMG_3461.MOV", 3.2, 6.2, {}), ("IMG_3478.MOV", 0.5, 2.5, {}), ("novo_IMG_3474.MOV", 2.4, 4.4, {}), ("IMG_3475.MOV", 2.6, 4.4, {}),
  ("almoco.MOV", 0.2, 2.4, {}),
  ("novo_painel_37a4ecb5.mov", 1.0, 2.9, {"girar": "transpose=2", "cx": 0.46}), ("IMG_3480.MOV", 1.5, 4.0, {}), ("IMG_3493.MOV", 6.3, 8.5, {}),
  ("janta.MOV", 7.4, 9.8, {}),
  ("volta1.MOV", 4.5, 6.8, {}), ("volta2.MOV", 8.0, 11.0, {}),
]
