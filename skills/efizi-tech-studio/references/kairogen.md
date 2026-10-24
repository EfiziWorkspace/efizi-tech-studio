# Cenas e imagens com IA na Kairogen

Kairogen (kairogen.ai) é um agregador de modelos de imagem e vídeo com conector MCP para o Claude. Usar **só** para o
que precisa parecer filmado e não existe em material real nem dá para fazer em código (cenário, objeto físico).
Material real vence; motion em código vence IA.

## Regra de dinheiro

Cada geração gasta crédito. Antes de gerar:
1. `get_me_context` (plano e créditos) → `list_models` (parâmetros do modelo) → `estimate_cost` com os **mesmos**
   parâmetros que vai usar.
2. Dizer o custo a quem pediu e esperar o **ok**, a cada lote.
3. Passar `expected_credits` igual à cotação (o servidor recusa se o preço mudar — e não cobra).

Custos medidos (plano PRO, out/2026): imagem `nano-banana-2` 1k = **3 créditos**; vídeo `seedance-2-0-mini` 5 s 720p
sem áudio, a partir de imagem = **27 créditos**. 1 crédito ≈ R$ 0,16 nesse plano.

## Receita que funcionou: cenário animado 9:16

1. **Imagem primeiro** (aprovação barata): `generate_image`, modelo `nano-banana-2`, `extra_params: {"aspect_ratio": "9:16"}`,
   `wait_for_completion: true`. Prompt em inglês, descrevendo composição para o vertical: o elemento principal na
   metade de **cima** (a pessoa vai na frente, embaixo), centro livre, "no text, no logos, no people".
2. **Animar**: `generate_video`, `seedance-2-0-mini`, `first_frame_url` = URL da imagem, `aspect_ratio: "9:16"`,
   `duration_seconds: 5`, `resolution: "720p"`, `generate_audio: false` (áudio quase dobra o preço). Prompt de
   movimento: o que se mexe, câmera lenta, "no camera shake, no text". Leva 3–10 min.
3. Baixar (`curl` da URL de saída) para `referencia/`, cortar o trecho útil e subir para 1458×2592 com lanczos
   (zoom 1,35× no 1080×1920 permite mover a câmera do cenário).

Armadilhas medidas:
- `negative_prompt` e `aspect_ratio` como argumento direto deram erro de validação no `nano-banana-2`: usar
  `extra_params.aspect_ratio` e pôr as exclusões no texto do prompt.
- `extra_params.image` foi recusado no `seedance-2-0-mini`: usar `first_frame_url`.
- Saída é 720p: serve para fundo, não para primeiro plano.

## Direito autoral

Personagem, logo, figurino ou trilha de filme/série/marca de terceiros **não** entram, nem "parecido". Pedir
"original design, not any existing movie character" no prompt e conferir o resultado. Para o "clima de filme",
descrever o clima (cidade em ruínas, céu vermelho, robô de olhos vermelhos), não o personagem.

## Outros usos que funcionaram

- Iceberg subindo atrás da pessoa ("ponta do iceberg"), com cena gelada — imagem animada, 3 créditos de imagem.
- Avatar/produto: preferir recorte da tela real ou o modelo 3D do site a gerar.
- Vozes prontas de alguns agregadores falam português de Portugal: para narração em PT-BR, voz brasileira gravada ou
  clonada com autorização escrita da dona da voz.
