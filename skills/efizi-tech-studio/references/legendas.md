# Legendas

A legenda não é acessório: no feed, a maioria assiste sem som, então a legenda **é** o áudio para
essa pessoa. Ela também segura o olho no centro da tela.

## Como gerar

1. Transcreva sempre com idioma explícito. Padrão desta skill: `npx hyperframes transcribe <arquivo> --engine parakeet
   --language pt` (instale uma vez com `npx hyperframes models install parakeet`). Com o Whisper, o modelo padrão
   `small.en` traduz para inglês sem avisar:

   ```bash
   npx hyperframes transcribe cortado.mp4 -d . --json --model small --language pt
   ```

   Áudio com ruído ou música: `--model medium --language pt`.
2. Leia o `transcript.json` inteiro antes de legendar. Se tiver frase sem sentido, a transcrição
   errou: tente `medium` uma vez; se continuar ruim, avise em vez de legendar palavra inventada.
3. Corrija os termos técnicos pelo glossário abaixo, mudando só o `text` de cada palavra e mantendo
   `start` e `end`.
4. Monte a trilha de legenda dentro da composição, seguindo
   `hyperframes/skills/media-use/audio/references/captions/authoring.md`.

## Estilo do canal

| Item | Reels / Shorts (1080×1920) | YouTube longo (1920×1080) |
| --- | --- | --- |
| Palavras por grupo | 2–3 | 3–5 |
| Fonte | a de `caption` no `frame.md` (Manrope 800) | a mesma, peso 700 |
| Tamanho | 64–80 px | 48–56 px |
| Posição | centro horizontal, por volta de 62–68% da altura | terço inferior, acima de 85% da altura |
| Animação | palavra ativa acende na cor de ênfase; entrada curta (0,1–0,2 s) | palavra ativa acende; entrada suave (0,2–0,3 s) |
| Contraste | texto claro com contorno ou sombra escura, sempre legível sobre qualquer fundo | igual |

- **Manchete fixa (formato A):** além da legenda, a frase do gancho fica no topo o vídeo todo, Manrope 800 em
  caixa alta, branca, ~64 px em 1080 de largura, dentro da área segura (abaixo de 220 px do topo).
- **Palavra por palavra no centro (formatos A e C):** uma a três palavras por vez, no meio da tela, como nos
  modelos 2 e 3. A ênfase dos modelos usa uma segunda fonte (serifa itálica); a marca da Efizi não tem serifa,
  então aqui a ênfase é **laranja + escala 1,15** na palavra.
- **Palavra-chave em destaque:** nomes de ferramenta, números e a palavra principal da frase ficam
  na cor de ênfase. No máximo uma por grupo.
- **Números como números:** "dois mil e vinte e seis" vira "2026"; "cinquenta por cento" vira "50%".
- **Sem pontuação final** nos grupos curtos; vírgula e ponto só atrapalham a leitura rápida.
- **Vícios não aparecem:** "é…", "tipo", "né" que sobraram do corte não entram na legenda.
- Cada grupo fica pelo menos **0,5 s** na tela. Menos que isso ninguém lê.
- A legenda nunca fica embaixo de um cartão ou print. Quando um visual ocupa o lugar dela, ela sobe
  ou desce, mas não some.

## Glossário de correção (Whisper erra muito termo técnico em português)

Corrija para a grafia da direita. Acrescente aqui todo termo novo que aparecer errado.

| O Whisper escreve | Correto |
| --- | --- |
| a pi, api, ei pi ai | API |
| chat gpt, chat gepeto | ChatGPT |
| clode, cloud (quando fala do modelo) | Claude |
| ene oito ene, n oito n | n8n |
| postgres, póstgres | PostgreSQL |
| git hub, guite hub | GitHub |
| vs code, vê esse code | VS Code |
| linux, línux | Linux |
| front end / back end | front-end / back-end |
| deploy, diploi | deploy |
| prompt, prômpti | prompt |
| i a, ia | IA |
| wi fi, uai fai | Wi-Fi |
| python, páiton | Python |
| java script | JavaScript |
