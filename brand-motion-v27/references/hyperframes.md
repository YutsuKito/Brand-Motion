# HyperFrames no Brand Motion V27

Esta skill usa **HyperFrames como caminho preferencial para novos projetos**, mantendo **Python/Playwright/FFmpeg como fallback**. O exportador transforma manifests Brand Motion em composição HTML seekable e preserva as fases de explicação, zoom centralizado, navegação e CTA. Não converte screenshots em um site navegável real nem inventa cliques. Use alvos de clique apenas quando verificados.

## Requisitos e downloads

- Node.js >= 22: https://nodejs.org/en/download
- FFmpeg + FFprobe: https://ffmpeg.org/download.html
- CLI HyperFrames: https://github.com/heygen-com/hyperframes
- Skills oficiais: https://github.com/heygen-com/hyperframes (instale com permissão do usuário)
- Python 3.10+ para o exportador e manifests da Brand Motion.
- O exportador usa GSAP 3.14.2 e registra uma timeline pausada em `window.__timelines["brand-motion-v27"]`. Essa timeline avança o estado da composição por tempo absoluto, conforme o fluxo nativo do HyperFrames.

Instalar a skill Brand Motion não instala automaticamente HyperFrames nem Node. Confirme com o usuário antes de executar downloads ou instalações.

## Fluxo recomendado

Na raiz do repositório Brand-Motion:

~~~bash
node --version
ffmpeg -version
npm install -g hyperframes
npx skills add heygen-com/hyperframes
npx hyperframes doctor
npx hyperframes init meu-video --example blank
python brand-motion-v27/scripts/validate_project.py --config brand-motion-v27/examples/demo-saas/manifest.json
python brand-motion-v27/scripts/export_hyperframes.py --config brand-motion-v27/examples/demo-saas/manifest.json --project meu-video --replace
cd meu-video
npx hyperframes lint
npx hyperframes preview
npx hyperframes render --output final.mp4 --fps 30 --quality high
~~~

No Windows PowerShell, use os mesmos comandos; caso Python seja exposto pelo lançador Windows, use py em vez de python. O init cria a estrutura com meta.json, index.html e assets/. O exportador sobrescreve index.html apenas com --replace; faça backup caso já o tenha editado.

Para áudio com licença comercial confirmada, adicione ao comando do exportador: --audio caminho/da/faixa.wav. O arquivo será copiado para a pasta assets e incluído como faixa de áudio. Sons de clique devem corresponder aos tempos da timeline; uma faixa externa sem cliques não cria sincronismo automaticamente.

## Timeline HyperFrames

O exportador adiciona `data-composition-id`, início e dimensões ao elemento raiz; a duração vem da timeline pausada registrada pelo mesmo ID. O callback chama `window.seek(time)`, que calcula o estado visual completo para qualquer instante sem depender do relógio. Não use `data-no-timeline` nem `data-duration` no root: a timeline registrada define a duração para lint, preview e render.

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

As imagens dos exemplos são fictícias. Substitua-as por fotos e capturas autorizadas antes de publicar.

## Diagnóstico e QA

~~~bash
npx hyperframes doctor
npx hyperframes lint
npx hyperframes render --output final.mp4 --quality high
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of json final.mp4
~~~

Inspecione visivelmente quadros de títulos e acentos, interface sem cortes, centro exato do zoom, alvo do cursor, sons de clique, abertura de página após o clique e CTA final. Renderizar sem erros não substitui QA visual.

## Fallback sem HyperFrames

~~~bash
python -m pip install -r brand-motion-v27/requirements.txt
python -m playwright install chromium
python brand-motion-v27/scripts/render_video.py --config brand-motion-v27/examples/demo-saas/manifest.json --output output/demo --allow-placeholders
~~~

Use fallback quando o motor HyperFrames não puder ser instalado ou quando lint/render não forem aprovados. Informe qual motor produziu o MP4.

## Estado de validação

O exportador foi validado com HyperFrames CLI 0.8.217: doctor, preview e render; lint terminou com zero erros e um aviso de descoberta duplicada de imagens. O MP4 de teste ficou em 1920x1080, 30 fps, 21,8 s e 654 quadros, com H.264. O QA da skill reportou áudio ausente porque o manifest de exemplo não fornece uma faixa; o exportador inclui áudio quando recebe `--audio`. O teste ficou isolado em `work/brand-motion-test` e não usou o renderizador Python.

Documentação oficial: https://hyperframes.app/docs/5-packages/cli | https://hyperframes.app/docs/5-packages/engine | https://hyperframes.app/docs/3-guides/4-rendering
