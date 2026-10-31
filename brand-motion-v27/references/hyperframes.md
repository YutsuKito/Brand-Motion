# HyperFrames no Brand Motion V27

Esta skill exige **HyperFrames + GSAP + Three.js** em todo MP4 final. O exportador transforma manifests Brand Motion em composição HTML seekable, registra uma timeline GSAP pausada e adiciona um elemento Three.js cujo desenho é atualizado pelo mesmo tempo da timeline. Não converte screenshots em um site navegável real nem inventa cliques. Use alvos de clique apenas quando verificados.

## Requisitos e downloads

- Node.js >= 22: https://nodejs.org/en/download
- FFmpeg + FFprobe: https://ffmpeg.org/download.html
- CLI HyperFrames: https://github.com/heygen-com/hyperframes
- GSAP e Three.js instalados localmente no projeto: https://gsap.com/docs/v3/ e https://threejs.org/docs/
- Python 3.10+ para o exportador e manifests da Brand Motion.
- O exportador carrega `assets/gsap.min.js` e os módulos Three.js copiados para `assets/three/`; não use CDN nem rede durante o render.
- A timeline pausada fica em `window.__timelines["brand-motion-v27"]`. GSAP conduz `window.seek(t)` e cada chamada atualiza o Three.js para o mesmo instante.

Instalar esta skill não instala os motores. Verifique o que já existe e peça consentimento antes de baixar ou instalar dependências. Se faltar qualquer parte do stack obrigatório e a instalação não for autorizada, não produza um MP4 final por outro motor.

## Fluxo recomendado

Na pasta do projeto de vídeo, depois do briefing e da autorização para instalar dependências ausentes:

~~~bash
node --version
ffmpeg -version
npm install --save-exact hyperframes gsap three
npx hyperframes doctor
npx hyperframes init meu-video --example blank
python CAMINHO_DA_SKILL/scripts/validate_project.py --config CAMINHO_DO_PROJETO/manifest.json
python CAMINHO_DA_SKILL/scripts/export_hyperframes.py --config CAMINHO_DO_PROJETO/manifest.json --project meu-video --replace
cd meu-video
npx hyperframes check --json
npx hyperframes preview
npx hyperframes render --output final.mp4 --fps 30 --quality delivery
~~~

No Windows PowerShell, use os mesmos comandos; caso Python seja exposto pelo lançador Windows, use `py` em vez de `python`. O init cria a estrutura com meta.json, index.html e assets/. O exportador exige GSAP e Three.js instalados localmente e copia os módulos usados para `assets/`; também aceita `--three-build CAMINHO` quando a pasta `node_modules/three/build` não for padrão. Ele sobrescreve index.html apenas com `--replace`; faça backup caso já o tenha editado.

Para áudio com licença comercial confirmada, adicione ao comando do exportador: --audio caminho/da/faixa.wav. O arquivo será copiado para a pasta assets e incluído como faixa de áudio. Sons de clique devem corresponder aos tempos da timeline; uma faixa externa sem cliques não cria sincronismo automaticamente.

## Timeline HyperFrames

O exportador adiciona `data-composition-id`, início e dimensões ao elemento raiz; a duração vem da timeline pausada registrada pelo mesmo ID. O callback chama `window.seek(time)`, que calcula o estado visual e atualiza Three.js para qualquer instante sem depender do relógio. O módulo usa `window.__hf.buildReady` para concluir o setup antes do frame 0. Não use `data-no-timeline` nem `data-duration` no root: a timeline registrada define a duração para check, preview e render.

~~~js
const driver = { time: 0 };
const timeline = gsap.timeline({ paused: true });
timeline.to(driver, {
  time: 37, duration: 37, ease: "none",
  onUpdate() { window.seek(driver.time); }
});
window.__timelines["brand-motion-v27"] = timeline;
~~~

Cada quadro deve ser construído por tempo absoluto. O estilo V27 utiliza 4s de texto, 3,5s de zoom ao centro geométrico (960,540 para 1920x1080), ~0,9s de retorno/clique/navegação, depois CTA isolado. Não mova a UI simultaneamente com texto sendo lido.

Use `assets/gsap.min.js` em script local. A composição carrega Three.js via ES module local e expõe `renderAt(t)`. `window.seek(t)` chama esse renderer em cada quadro. Não use `requestAnimationFrame`, `setTimeout`, relógio do sistema nem aleatoriedade não-semeada; o resultado de qualquer timestamp precisa ser idêntico em preview e render.

Todo filme inclui pelo menos um elemento 3D útil para a identidade, produto ou referência. Para uma referência de motion 2D, mantenha o elemento 3D pequeno e integrado à linguagem visual, sem competir com o produto. Adapte geometria, material, luz e trajetória ao styleboard.

As imagens dos exemplos são fictícias. Substitua-as por fotos e capturas autorizadas antes de publicar.

## Diagnóstico e QA

~~~bash
npx hyperframes doctor
npx hyperframes check --json
npx hyperframes render --output final.mp4 --quality delivery
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of json final.mp4
~~~

Inspecione visivelmente os quadros de títulos e acentos, interface sem cortes, centro exato do zoom, acento 3D, alvo do cursor, sons de clique, abertura de página após o clique e CTA final. Renderizar sem erros não substitui QA visual.

## Se o stack obrigatório estiver indisponível

Não troque o render final por Python, Playwright ou FFmpeg. Peça autorização para instalar o componente ausente ou entregue o diagnóstico e aguarde; scripts Python e FFmpeg continuam disponíveis para inspeção, extração de frames e QA.

Documentação oficial: https://hyperframes.app/docs/5-packages/cli | https://hyperframes.app/docs/5-packages/engine | https://hyperframes.app/docs/3-guides/4-rendering

