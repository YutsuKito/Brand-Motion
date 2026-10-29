---
name: brand-motion-v27
description: Produz vídeos comerciais demonstrativos para SaaS, aplicativos, sites, lojas e produtos físicos no estilo V27: texto breve por 4 s, zoom do produto centralizado por 3,5 s, navegação sincronizada, CTA e exportação MP4 com QA. Use quando alguém pedir vídeo de produto ou apresentação animada com imagens, interfaces ou motion graphics.
compatibility: Codex, Claude Code, OpenCode, Hermes e agentes que leem Agent Skills SKILL.md e podem executar Python, Chromium e FFmpeg.
metadata:
  format: "16:9"
  engine: hyperframes-preferred; playwright-ffmpeg-fallback
  version: "1.0.0"
---

# Brand Motion V27 — produção universal de vídeos

## Primeiro contato: briefing, sem começar a inventar

Faça perguntas curtas ao usuário **apenas sobre dados ainda desconhecidos** e aceite respostas parciais. Se já houver informações ou anexos, use-os sem pedir novamente. Perguntas prioritárias:

1. **Qual marca/produto/serviço?** Nome, site oficial e o que vende/oferece.
2. **Qual o objetivo e CTA?** Demonstrar, vender, divulgar, testar grátis, comprar, conhecer planos, reservar etc. Confirme ofertas e URLs.
3. **Quais materiais reais existem?** Peça logo/favicon, capturas de telas, imagens do produto, fotos do estabelecimento, vídeos ou link do site. Pergunte se pode usar esses assets na peça.
4. **Há referência visual?** Peça um vídeo, link, imagem ou exemplo de estilo. Explique o estilo V27 descrito nesta skill e peça referências visuais próprias do usuário, sem impor identidade de outra marca.
5. **Onde vai publicar?** Por padrão entregue 16:9, 1920×1080, 30 FPS; pergunte quando houver preferência diferente de formato/duração, idioma ou trilha.

Se faltar uma imagem essencial e não houver ferramenta de captação/geração permitida, use um placeholder **apenas na prévia** e informe o que falta para uma versão final. Não reproduza slogans, ofertas, preços, logos, pessoas ou resultados não verificados.

## Estilo inegociável da V27

- **Fase A (4,0 s)**: produto/website à direita, título com curta digitação; descrição de 1 frase aparecendo inteira por fade, depois texto estacionário. Não mova o aplicativo enquanto alguém lê.
- **Fase B (3,5 s)**: remova completamente título e explicação; desloque e amplie o produto para o **centro geométrico do quadro**, em 1920×1080 exatamente `x=960, y=540`, sem recortes; mantenha para observação.
- **Fase C (~0,9 s)**: reduza/retorne ao enquadramento lateral; quando for demo de UI e houver alvo validado, mova o mouse ao controle certo, clique, reproduza som no mesmo instante, e **só depois** revele a nova página. Sem alvo confirmado, transição sem cursor/click sound.
- **Final (~5 s)**: feche/retire a interface; fundo claro; marca, CTA principal, CTA secundário opcional, domínio e nuvens discretas atrás do conteúdo. CTA isolado e legível.
- Não use boxes gigantes, destaques/retângulos nos campos, nem motion simultâneo ao texto; o software ou produto deve ser protagonista. Texto nunca se sobrepõe ao conteúdo.

## Motor de vídeo: HyperFrames preferencial

Para novos projetos, **priorize HyperFrames oficial**, não afirme usá-lo quando o MP4 foi produzido com o fallback. Antes de executar downloads ou instalações, peça consentimento. Siga [references/hyperframes.md](references/hyperframes.md): Node.js 22+, FFmpeg, HyperFrames CLI e skills oficiais do HyperFrames. O motor aceita composições HTML seekable pelo protocolo window.__hf; o exportador da Brand Motion gera uma composição a partir do manifest e utiliza os mesmos 4s explicação / 3,5s zoom centralizado / retorno / CTA.

Fluxo preferencial após briefing, assets e validação do manifest:

~~~bash
npx hyperframes doctor
npx hyperframes init meu-video --example blank
python scripts/export_hyperframes.py --config CAMINHO/manifest.json --project meu-video --replace
cd meu-video
npx hyperframes lint
npx hyperframes preview
npx hyperframes render --output final.mp4 --fps 30 --quality high
~~~

Os caminhos relativos variam conforme a pasta do agente; use o caminho real do script. Não reutilize as imagens fictícias dos exemplos como se fossem telas da marca. Quando o CLI estiver indisponível ou falhar, documente a falha e use o renderizador Python (passos abaixo) somente como fallback. O exportador HyperFrames foi implementado, mas o CLI não pôde ser testado neste ambiente; nunca o declare validado sem rodar lint/render/QA na máquina de destino.

## Pipeline obrigatório

1. **Auditar ambiente:** rode `npx hyperframes doctor` para o modo preferencial e `python scripts/doctor.py` para o fallback. Consulte `references/dependencies.md`; instalar somente com consentimento, conferindo licenças e permissões. Verifique Python, Playwright/Chromium, Pillow, NumPy e FFmpeg. Nunca force instalação de browser em máquina corporativa.
2. **Pesquisar e coletar:** use materiais do cliente primeiro. Faça capturas do site apenas se a ferramenta e as permissões de acesso existirem. Documente fontes/licenças em `assets-ledger.csv`. Jamais remova marcas d'água nem use imagens protegidas sem licença. Se for UI autenticada, solicite screenshots ou acesso aprovado, sem pedir senhas em chat.
3. **Roteirizar:** 3 a 7 cenas (painel, função, benefício, exemplo, relatório etc.), cada uma com título curto, uma frase descritiva e imagem/tela associada. Para lojas e produtos físicos, use fotografia/B-roll e movimento de câmera, **não simule cliques**.
4. **Preparar projeto:** copie `templates/project.example.json` e `templates/assets` para uma pasta de produção. Atualize marca, site, ícones, imagens e cenas. O arquivo `manifest.json` é a única fonte de duração, texto, CTA, assets e navegação do template genérico.
5. **Validar fontes e timeline:** `python scripts/validate_project.py --config caminho/manifest.json`. As telas devem ser reais ou identificadas como ilustrações. Para clique, registre alvo `click_target` normalizado e verificado manualmente na **imagem da cena de origem** (ex.: item Aplicações). Se não houver essa confirmação, omita o clique.
6. **Gerar prévia** com `npx hyperframes preview` no projeto exportado; para fallback use `python scripts/render_video.py --config caminho/manifest.json --output caminho/output --preview-only`. Examine abertura, pontos de foco, trocas de cena, último quadro e CTA. Ajuste composições antes de renderizar tudo.
7. **Renderizar:** use HyperFrames como padrão (comandos acima). Quando não estiver disponível, execute o fallback com `python scripts/render_video.py --config caminho/manifest.json --output caminho/output`. Use FFmpeg H.264/AAC e música original gerada localmente, ou faixa externa com licença confirmada. Exporte MP4, contact sheet, timeline e QA.
8. **QA final:** executar `python scripts/qa.py --video caminho/output/final.mp4 --config caminho/manifest.json`. Verifique 16:9, duração, FPS, áudio, quadro centralizado, clipping, sincronismo click/evento, fontes, CTA e reprodução; não declare aprovado aquilo que não foi testado.
9. **Entregar** MP4, storyboard, assets com proveniência, projeto editável e sumário das verificações. Sem afirmar ser gravação ao vivo se for reconstrução ilustrativa.

## Modo de composição

- `kind: "software"`: screenshot de site, SaaS ou app dentro de uma janela de navegador, com ponteiro opcional baseado em `click_target`. Se for componente DOM real, o agente pode adaptar o código V27 para localizar elementos via `getBoundingClientRect()`; o template universal trabalha com screenshots verificadas, não cliques verdadeiros em site.
- `kind: "product"`: fotografia de produto (centraliza/zoom e transições, sem cursor).
- `kind: "store"`: imagens de loja, vitrines, pratos/serviços ou e-commerce (sem cursor salvo demonstração real de interface).
- `kind: "service"`: local/serviço e imagens reais de execução, sem promessas inventadas.

Leia `references/storyboard.md` e `references/qa-checklist.md` antes de renderizar. Se a marca exigir animações mais avançadas ou vídeo real, integre assets gerados por ferramentas apropriadas; o motor incluído é um **baseline confiável de motion 2D** e não substitui geradores 3D/video-to-video.

## Compatibilidade e montagem

A skill usa o padrão aberto **Agent Skills**, `SKILL.md` com YAML. Um mesmo conteúdo funciona em Codex, Claude Code, OpenCode e Hermes **quando esses agentes permitem executar os scripts e acessar os arquivos**. A instalação é feita por `scripts/install_skill.py`; consulte `references/install-agents.md` para pastas e procedimentos (instalação por projeto ou usuário). Não pressupor que todos os agentes têm navegador, permissão de shell ou credenciais.

## Referência do estilo V27

A técnica é inspirada no padrão de produção V27: explicação por 4 segundos, foco geométrico com zoom por 3,5 segundos, clique sincronizado em demonstrações de software e CTA isolado. Este pacote **não** inclui vídeo, telas, logos nem código proprietário de uma marca. Use apenas imagens fornecidas/autorizadas pelo usuário e substitua os SVGs de exemplo antes de publicar.
