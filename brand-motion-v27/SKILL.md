---
name: brand-motion-v27
description: Produz vídeos comerciais demonstrativos para SaaS, aplicativos, sites, lojas e produtos físicos no estilo V27. Usa HyperFrames, GSAP e Three.js; analisa vídeos de referência e recria sua linguagem visual com assets autorizados ou originais. Use para vídeos de produto e motion graphics.
metadata:
  format: "16:9"
  engine: hyperframes-required; gsap-required; threejs-required
  version: "1.1.0"
---

# Brand Motion V27 — produção universal de vídeos

## Primeiro contato: briefing, sem começar a inventar

### Comportamento obrigatório ao iniciar uma produção

Quando o usuário apenas acionar a skill, **não comece a renderizar e não assuma uma marca fictícia**. Inicie uma conversa breve para coletar o mínimo necessário. A primeira pergunta deve estabelecer **marca/produto + site ou descrição**. Depois peça **materiais visuais reais ou links de referência**, **objetivo/CTA** e **formato/duração** somente se ainda estiverem ausentes. Aceite respostas parciais, uma conversa por vez; não use um formulário longo ou exija tudo de uma só vez.

Se o usuário já forneceu marca, site, screenshots, produto e CTA, não repita as perguntas; confirme apenas lacunas essenciais (como permissão de uso das imagens) antes de executar. Não gere o MP4 final com placeholders. Pode montar roteiro e storyboard preliminares, desde que os elementos fictícios sejam claramente indicados.

**Exemplo de primeira resposta sem briefing:**
> Qual marca ou produto você quer apresentar? Pode enviar o site ou uma descrição rápida. Depois vou pedir as imagens, telas ou referências visuais para montar o vídeo.

Ao receber a marca/site:
> Você tem logo, fotos ou capturas da aplicação, ou links de vídeos cujo estilo deseja seguir? Posso usar esses materiais no vídeo?

Antes da produção final, confirme o CTA e a página de destino, se aplicáveis, e registre a licença/proveniência dos assets.


Faça perguntas curtas ao usuário **apenas sobre dados ainda desconhecidos** e aceite respostas parciais. Se já houver informações ou anexos, use-os sem pedir novamente. Perguntas prioritárias:

1. **Qual marca/produto/serviço?** Nome, site oficial e o que vende/oferece.
2. **Qual o objetivo e CTA?** Demonstrar, vender, divulgar, testar grátis, comprar, conhecer planos, reservar etc. Confirme ofertas e URLs.
3. **Quais materiais reais existem?** Peça logo/favicon, capturas de telas, imagens do produto, fotos do estabelecimento, vídeos ou link do site. Pergunte se pode usar esses assets na peça.
4. **Há referência visual?** Se o usuário anexou um vídeo, analise-o sem pedir outra referência. Caso contrário, peça um vídeo, link ou imagem; pergunte se ele quer reutilizar assets exatos da referência ou apenas recriar a linguagem visual.
5. **Onde vai publicar?** Por padrão entregue 16:9, 1920×1080, 30 FPS; pergunte quando houver preferência diferente de formato/duração, idioma ou trilha.

Se faltar uma imagem essencial e não houver ferramenta de captação/geração permitida, use um placeholder **apenas na prévia** e informe o que falta para uma versão final. Não reproduza slogans, ofertas, preços, logos, pessoas ou resultados não verificados.

## Vídeo de referência

Quando o usuário enviar um vídeo, leia [references/style-reference.md](references/style-reference.md) e faça a análise visual antes de desenhar cenas. Preserve a sequência V27 e adapte ao vídeo o ritmo, a paleta, a tipografia, a composição, as transições, a iluminação e os motion graphics. Reutilize os assets do vídeo apenas quando o usuário tiver direito de uso; caso contrário, crie alternativas originais com linguagem visual semelhante. Registre a origem e a licença de cada asset.

## Estilo inegociável da V27

- **Fase A (4,0 s)**: produto/website à direita, título com curta digitação; descrição de 1 frase aparecendo inteira por fade, depois texto estacionário. Não mova o aplicativo enquanto alguém lê.
- **Fase B (3,5 s)**: remova completamente título e explicação; desloque e amplie o produto para o **centro geométrico do quadro**, em 1920×1080 exatamente `x=960, y=540`, sem recortes; mantenha para observação.
- **Fase C (~0,9 s)**: reduza/retorne ao enquadramento lateral; quando for demo de UI e houver alvo validado, mova o mouse ao controle certo, clique, reproduza som no mesmo instante, e **só depois** revele a nova página. Sem alvo confirmado, transição sem cursor/click sound.
- **Final (~5 s)**: feche/retire a interface; fundo claro; marca, CTA principal, CTA secundário opcional, domínio e nuvens discretas atrás do conteúdo. CTA isolado e legível.
- Não use boxes gigantes, destaques/retângulos nos campos, nem motion simultâneo ao texto; o software ou produto deve ser protagonista. Texto nunca se sobrepõe ao conteúdo.

## Motor obrigatório: HyperFrames + GSAP + Three.js

Todo MP4 final deve ser produzido com **HyperFrames**, com uma timeline **GSAP** pausada e registrada, e pelo menos um elemento 3D intencional renderizado com **Three.js**. HyperFrames controla composição, busca e render; GSAP dirige o tempo; Three.js desenha o elemento 3D. O Three.js deve refletir o produto ou a referência, sem virar decoração genérica: quando o vídeo de referência for 2D, use um acento 3D discreto, como profundidade em um símbolo ou objeto da marca.

Antes de instalar dependências, peça consentimento. Use arquivos locais e versões fixadas pelo lockfile; não use CDN ou requisições de rede durante a composição/render. Se o stack estiver ausente e o usuário não autorizar a instalação, pare antes do MP4 final e explique o bloqueio. O renderizador Python/Playwright é legado e não substitui o stack obrigatório.

Siga [references/hyperframes.md](references/hyperframes.md). O exportador gera uma composição a partir do manifest, carrega GSAP e Three.js localmente e liga `window.seek(time)` ao render do Three.js. Toda imagem deve ser função determinística do tempo recebido, sem relógio, timers ou loop autônomo.

Fluxo obrigatório após briefing, análise de referência, assets e validação do manifest:

~~~bash
npx hyperframes doctor
npx hyperframes init meu-video --example blank
npm install --save-exact hyperframes gsap three
python scripts/export_hyperframes.py --config CAMINHO/manifest.json --project meu-video --replace
cd meu-video
npx hyperframes check --json
npx hyperframes preview
npx hyperframes render --output final.mp4 --fps 30 --quality delivery
~~~

Os caminhos relativos variam conforme a pasta do agente; use o caminho real do script. Instale apenas dependências ausentes e só depois do consentimento. Não reutilize as imagens fictícias dos exemplos como se fossem telas da marca. Não use renderizador alternativo para o MP4 final. Execute `check`, prévia e render HyperFrames; depois inspecione abertura, foco, navegação, acento 3D e CTA.

## Pipeline obrigatório

1. **Auditar o stack:** rode `npx hyperframes doctor`, confirme GSAP e Three.js no projeto e consulte `references/dependencies.md`. Instale somente o que faltar, após consentimento. Python pode apoiar inspeção e QA; não use outro motor para o MP4 final.
2. **Analisar referência e coletar assets:** para vídeo de referência, aplique `references/style-reference.md`. Use materiais do cliente primeiro, registre origem/licença em `assets-ledger.csv` e não reutilize elementos protegidos sem autorização. Faça capturas de site somente com acesso permitido; nunca peça senhas em chat.
3. **Roteirizar:** crie 3 a 7 cenas com título curto, frase descritiva e imagem/tela associada. Preserve o ritmo e a linguagem visual da referência, sem alterar a estrutura V27. Planeje pelo menos um elemento 3D Three.js conectado à marca/produto. Para lojas e produtos físicos, use fotografia/B-roll e movimento de câmera; não simule cliques.
4. **Preparar projeto:** copie `templates/project.example.json` e os assets autorizados para a pasta de produção. Atualize marca, site, ícones, imagens e cenas. O manifest é a fonte de duração, texto, CTA, assets e navegação; o storyboard/styleboard registra as escolhas de design.
5. **Validar fontes e timeline:** rode `python scripts/validate_project.py --config caminho/manifest.json`. Garanta GSAP local, módulo Three.js local e timeline seekable. Para clique, confirme manualmente o alvo na imagem da cena; sem confirmação, omita clique e som.
6. **Pré-visualizar:** use `npx hyperframes preview` e `npx hyperframes snapshot --review`. Examine abertura, foco, transições, movimento 3D, último quadro e CTA. Ajuste a composição antes do render final.
7. **Renderizar:** use apenas HyperFrames para o MP4 final. Use FFmpeg/ffprobe para inspeção, não como motor alternativo. Exporte MP4, contact sheet, timeline, QA e projeto editável.
8. **QA final:** execute `python scripts/qa.py --video caminho/output/final.mp4 --config caminho/manifest.json`. Verifique 16:9, duração, FPS, áudio, centro geométrico, clipping, sincronismo, fonts, CTA, consistência com a referência e render 3D sem flicker/falhas de seek. Não declare aprovado o que não foi testado.
9. **Entregar** MP4, storyboard/styleboard, assets com proveniência, projeto editável e resumo do QA. Sem afirmar ser gravação ao vivo se for reconstrução ilustrativa.

## Modo de composição

- `kind: "software"`: screenshot de site, SaaS ou app dentro de uma janela de navegador, com ponteiro opcional baseado em `click_target`. Se for componente DOM real, o agente pode adaptar o código V27 para localizar elementos via `getBoundingClientRect()`; o template universal trabalha com screenshots verificadas, não cliques verdadeiros em site.
- `kind: "product"`: fotografia de produto (centraliza/zoom e transições, sem cursor).
- `kind: "store"`: imagens de loja, vitrines, pratos/serviços ou e-commerce (sem cursor salvo demonstração real de interface).
- `kind: "service"`: local/serviço e imagens reais de execução, sem promessas inventadas.

Todo modo inclui um acento 3D Three.js ligado à identidade ou à referência; mantenha-o fora da área de leitura e do conteúdo essencial do produto. A cena Three.js precisa obedecer ao seek do HyperFrames por meio do tempo dirigido por GSAP.

Leia `references/storyboard.md` e `references/qa-checklist.md` antes de renderizar; com vídeo de referência, leia também `references/style-reference.md`. O Three.js fornece elementos 3D gerados na composição, mas não substitui um modelo/produto real: use arquivos autorizados ou identifique reconstruções ilustrativas.

## Compatibilidade e montagem

A skill usa o padrão aberto **Agent Skills**, `SKILL.md` com YAML. Um mesmo conteúdo funciona em Codex, Claude Code, OpenCode e Hermes **quando esses agentes permitem executar os scripts e acessar os arquivos**. A instalação é feita por `scripts/install_skill.py`; consulte `references/install-agents.md` para pastas e procedimentos (instalação por projeto ou usuário). Não pressupor que todos os agentes têm navegador, permissão de shell ou credenciais.

## Referência do estilo V27

A técnica é inspirada no padrão de produção V27: explicação por 4 segundos, foco geométrico com zoom por 3,5 segundos, clique sincronizado em demonstrações de software e CTA isolado. Este pacote **não** inclui vídeo, telas, logos nem código proprietário de uma marca. Use apenas imagens fornecidas/autorizadas pelo usuário e substitua os SVGs de exemplo antes de publicar.

