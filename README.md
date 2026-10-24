# Efizi Tech Studio

**A skill de edição de vídeo da Efizi Tech para o [Claude Code](https://claude.com/claude-code).** Você manda a
gravação, ela devolve o Reels pronto: takes escolhidos, cor de cinema, legenda pulando, telas com zoom e chicote,
cenário atrás da pessoa, efeitos com motivo, música que abaixa sozinha quando alguém fala — e confere a voz por número
antes de entregar.

Tudo aqui saiu de vídeos reais editados para o canal Efizi Tech, com cada "ficou feio", "demorou muito" e "bugou a
voz" transformado em regra. É montada em cima do [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen),
que transforma HTML em vídeo.

## O que ela faz

- **Takes e cortes:** escolhe a melhor tentativa de cada frase (fala inteira, entonação, olhar na câmera), corta no
  silêncio medido e emenda sem palavra picotada.
- **Cor:** LUT técnica para câmera Sony S-Log3 (calculada, sem arquivo de terceiros) + looks prontos (`efizi`, `tech`,
  `dourado`) + método para copiar a cor de um vídeo de referência medindo em Lab.
- **Pegada jovem:** legenda palavra por palavra que pula, punch nas palavras-chave, glitch nas viradas, objeto 3D
  saindo da ponta do dedo, cenário atrás da pessoa por 2–3 s, cérebro de pontos, "problema → aprendendo → salvo".
- **Telas:** gravação de tela entrando de chicote, zoom no que a pessoa cita, mouse andando até o botão com a câmera
  seguindo e clique com som.
- **Áudio:** música baixa com sidechain na voz (só aparece nas pausas), efeitos só com motivo, níveis medidos.
- **IA (opcional):** cenários e imagens na [Kairogen](https://kairogen.ai), com custo estimado e aprovado antes.
- **Conferência:** emendas, texto falado × roteiro e sincronia voz × boca medidos antes de entregar.

## Instalação

Precisa de: **Claude Code**, **Node 22+**, **FFmpeg 7+** no PATH, **Python 3.11+** e **Git**.
Testado com Node 24, FFmpeg 9, Python 3.12 e HyperFrames 0.8.177, no Windows 11.

1. Bibliotecas do Python:
   ```bash
   pip install numpy pillow
   ```
2. Skills do HyperFrames e o modelo de transcrição em português:
   ```bash
   npx hyperframes skills update
   ```
   ```bash
   npx hyperframes models install parakeet
   ```
3. Esta skill:
   ```bash
   git clone https://github.com/EfiziWorkspace/efizi-tech-studio
   ```
   E copie a pasta da skill para as skills do Claude Code:
   - Windows (PowerShell): `Copy-Item -Recurse efizi-tech-studio\skills\efizi-tech-studio $HOME\.claude\skills\`
   - macOS / Linux: `cp -r efizi-tech-studio/skills/efizi-tech-studio ~/.claude/skills/`
4. (Opcional) Conector da Kairogen no Claude, para gerar cenários com IA.

## Como usar

Abra o Claude Code numa pasta de trabalho e peça em português, do seu jeito:

- "Edita esse vídeo que eu gravei e transforma num Reels" (e diga onde está o arquivo)
- "Escolhe os melhores takes desse bruto e corta os silêncios"
- "Quero essa colorimetria" (com um print ou link do vídeo de referência)
- "Quando ela fala do agente, coloca um cenário apocalíptico atrás dela"
- "Mostra a tela só quando ela mexe, com zoom e um vuuu pro lado"
- "Coloca uma trilha tech bem baixinha que só aparece nas pausas"

A skill cria a pasta do vídeo (`scripts/novo_projeto.py`), mostra o roteiro antes de montar e renderiza em `saida/`.

## O que tem aqui

```
skills/efizi-tech-studio/
├── SKILL.md              o processo, as regras e o mapa das referências
├── references/           um arquivo por assunto: fluxo, takes, cor, recorte, telas, efeitos, áudio,
│                         Kairogen, entrega, lições, ganchos, retenção, legendas, formatos, modelos
├── scripts/              novo_projeto.py + os scripts copiados para cada vídeo (montagem, cor, telas,
│                         pessoa recortada, trilha, conferência de voz)
├── modelos/              frame.md (identidade), encerramento padrão, marca, fontes, arquivos do HyperFrames
└── exemplos/reels-agentes/   a composição completa de um Reels real (sem os vídeos), para copiar peças
```

Os scripts com dados de um vídeo específico (`telas.py`, `pessoa.py`, `montar_trilha.py`, `quadro.py`) dizem
"EXEMPLO" no topo: o Claude ajusta os tempos e medidas para o seu vídeo.

## Usar com outra marca

A identidade está toda em `modelos/frame.md` (cores, fontes, logo) e `references/marca-efizi-tech.md`. Troque esses
dois pela sua marca; o processo, a cor, os efeitos e a conferência continuam iguais.

## Licença

Código e textos: MIT (ver `LICENSE`). O nome, a logo e a identidade **Efizi / Efizi Tech** são marcas da Efizi:
use-os só em conteúdo da Efizi. A fonte JetBrains Mono vai com a licença OFL dela. O HyperFrames é da HeyGen,
licença Apache 2.0.
