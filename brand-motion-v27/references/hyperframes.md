# HyperFrames no Brand Motion V27

Esta skill usa **HyperFrames como caminho preferencial para novos projetos**, mantendo **Python/Playwright/FFmpeg como fallback**. O exportador transforma manifests Brand Motion em composição HTML seekable e preserva as fases de explicação, zoom centralizado, navegação e CTA. Não converte screenshots em um site navegável real nem inventa cliques. Use alvos de clique apenas quando verificados.

## Requisitos e downloads

- Node.js >= 22: https://nodejs.org/en/download
- FFmpeg + FFprobe: https://ffmpeg.org/download.html
- CLI HyperFrames: https://github.com/heygen-com/hyperframes
- Skills oficiais: https://github.com/heygen-com/hyperframes (instale com permissão do usuário)
- Python 3.10+ para o exportador e manifests da Brand Motion.
- GSAP é opcional para novas animações. O exportador atual utiliza o protocolo window.__hf.seek(time) e não exige GSAP; ao adicionar GSAP, crie timelines pausadas e registre window.__timelines conforme os guias oficiais.

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

## Protocolo seekable

O exportador adiciona data-composition-id, atributos de tempo/dimensões ao elemento raiz e registra:

~~~js
window.__hf = {
  duration: 37,
  seek(time) { window.seek(time); }
};
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

O **exportador e a documentação** estão integrados, mas o CLI oficial não pôde ser executado neste ambiente porque o npm está inacessível. Agentes devem validar com doctor, lint, render e QA; se a versão instalada requerer alterações de protocolo, adaptar conforme a documentação e NÃO afirmar que passou antes de testar.

Documentação oficial: https://hyperframes.app/docs/5-packages/cli | https://hyperframes.app/docs/5-packages/engine | https://hyperframes.app/docs/3-guides/4-rendering
