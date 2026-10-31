# Brand Motion V27 — Skill universal para agentes IA

**Objetivo:** criar vídeos demonstrativos para **qualquer SaaS, loja, produto físico, site ou serviço** com o método V27 (4 segundos de explicação, 3,5 de zoom centralizado, troca sincronizada e CTA), em 16:9 Full HD.

A skill exige **HyperFrames + GSAP + Three.js** para cada MP4 final. Inclui exportador HTML seekable, áudio/SFX original, instalador para quatro agentes, exemplos e checklist. Vídeos de referência orientam a linguagem visual; assets exatos só são reutilizados com direitos confirmados.

## Instalação rápida — sem clone

Requer Node.js 22.20+. Para instalar globalmente em Claude Code, Codex, OpenCode e Hermes:

~~~powershell
npx skills add YutsuKito/Brand-Motion --skill brand-motion-v27 -g -a claude-code -a codex -a opencode -a hermes-agent -y
~~~

Para apenas um agente, troque a lista após -a, por exemplo: -a claude-code. Para instalar somente no projeto corrente, omita -g. Consulte [README principal](../README.md) e [instalação por agente](references/install-agents.md).

A CLI instala a **skill**, não os motores de renderização. Instale HyperFrames, GSAP, Three.js e FFmpeg separadamente após consentimento; valide o ambiente antes de produzir.

## 1 — Instalação manual/ZIP

Extraia este ZIP. Dentro da pasta que contém `brand-motion-v27/`:

```powershell
python .\brand-motion-v27\scripts\install_skill.py --agent all --scope user
```

No macOS/Linux:

```bash
python3 brand-motion-v27/scripts/install_skill.py --agent all --scope user
```

O instalador copia a skill para Codex, Claude Code, OpenCode e Hermes (sem exigir que todos estejam instalados). Consulte `references/install-agents.md`. Se quiser instalação por repositório, use `--scope project --root ./meu-projeto`.

## 2 — Stack obrigatório

Dependências: Node.js 22+, HyperFrames, GSAP, Three.js, FFmpeg e Python 3.10+ para exportar manifests. Verifique o que já existe e peça consentimento antes de instalar dependências ausentes:

~~~powershell
npm install --save-exact hyperframes gsap three
npx hyperframes doctor
npx hyperframes init meu-video --example blank
python .\brand-motion-v27\scripts\export_hyperframes.py --config .\brand-motion-v27\examples\demo-saas\manifest.json --project .\meu-video --replace
cd meu-video
npx hyperframes check --json
npx hyperframes preview
npx hyperframes render --output final.mp4 --fps 30 --quality delivery
~~~

Não anuncie os exemplos fictícios como dados reais. Consulte [references/hyperframes.md](references/hyperframes.md) para o protocolo de timeline HyperFrames, GSAP e Three.js.

## 3 — QA e inspeção

Python e FFmpeg podem validar manifests, analisar referências, extrair quadros e conferir o MP4 final. O renderizador Python/Playwright é legado e não substitui HyperFrames no arquivo final.

## 4 — Validar o render HyperFrames

```powershell
python scripts\validate_project.py --config examples\demo-saas\manifest.json
npx hyperframes check --json
npx hyperframes snapshot --review
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of json final.mp4
```

O exemplo usa capturas em SVG **fictícias** e não deve ser publicado como demonstração real de uma marca.

## 5 — Produzir para outra marca

Copie `templates/project.example.json` para `meu-video/manifest.json`; copie fotos, screenshots ou logos licenciados para `meu-video/assets/`, atualize as cenas e CTA. Abra `SKILL.md`, `references/storyboard.md` e `references/qa-checklist.md`. Se houver vídeo de referência, leia `references/style-reference.md` e analise o estilo antes de produzir.

**Prática recomendada:** peça ao agente: *“Use a skill brand-motion-v27; quero um vídeo de [minha marca]. Faça o briefing, analise minhas fotos/links e gere storyboard, MP4 e projeto.”*

### Notas

- A referência V27 é uma **metodologia de movimento e enquadramento**, não um asset de terceiros distribuído neste repositório.
- O envio de vídeo como referência permite analisar o estilo, mas não reutilizar automaticamente frames, músicas, logos ou outros assets.
- O navegador do projeto genérico usa imagens locais embutidas como `data:` URI, para evitar dependência de acesso externo durante render.
- Cliques em screenshots são **animações sincronizadas**, não interação autenticada com o site; coordenadas devem ser verificadas para corresponder ao elemento real na imagem.
- Os custos de ferramentas externas de imagem/vídeo, música premium ou APIs não estão incluídos; o baseline é local e sem API.
- Música sintetizada original, sem gravações de terceiros. Use faixa externa apenas com licença comprovada.

