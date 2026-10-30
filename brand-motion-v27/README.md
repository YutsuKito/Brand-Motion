# Brand Motion V27 — Skill universal para agentes IA

**Objetivo:** criar vídeos demonstrativos para **qualquer SaaS, loja, produto físico, site ou serviço** com o método V27 (4 segundos de explicação, 3,5 de zoom centralizado, troca sincronizada e CTA), em 16:9 Full HD.

A skill prioriza o **HyperFrames oficial (CLI)** para novos projetos e preserva um **fallback Python/Playwright/FFmpeg**. Inclui exportador HTML seekable, áudio/SFX original, instalador para quatro agentes, exemplos e checklist. O baseline é **motion 2D**, não gerador de vídeos realistas por IA.

## Instalação rápida — sem clone

Requer Node.js 22.20+. Para instalar globalmente em Claude Code, Codex, OpenCode e Hermes:

~~~powershell
npx skills add YutsuKito/Brand-Motion --skill brand-motion-v27 -g -a claude-code -a codex -a opencode -a hermes-agent -y
~~~

Para apenas um agente, troque a lista após -a, por exemplo: -a claude-code. Para instalar somente no projeto corrente, omita -g. Consulte [README principal](../README.md) e [instalação por agente](references/install-agents.md).

A CLI instala a **skill**, não os motores de renderização. Instale HyperFrames/FFmpeg/Python separadamente e valide o ambiente. O método por ZIP abaixo continua disponível como alternativa.

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

## 2 — Instalar HyperFrames (recomendado)

Dependências: Node.js 22+, FFmpeg e Python 3.10+ para exportar manifests. Com consentimento do usuário:

~~~powershell
npm install -g hyperframes
npx skills add heygen-com/hyperframes
npx hyperframes doctor
npx hyperframes init meu-video --example blank
python .\brand-motion-v27\scripts\export_hyperframes.py --config .\brand-motion-v27\examples\demo-saas\manifest.json --project .\meu-video --replace
cd meu-video
npx hyperframes lint
npx hyperframes preview
npx hyperframes render --output final.mp4 --fps 30 --quality high
~~~

Não anuncie os exemplos fictícios como dados reais. Consulte [references/hyperframes.md](references/hyperframes.md) para o protocolo de timeline HyperFrames e o relatório da validação local.

## 3 — Fallback Python/Playwright


É necessário **Python 3.10+**, **FFmpeg**, **Playwright**, **Chromium**, **Pillow** e **NumPy**. O agente deve pedir permissão antes de instalar; alguns ambientes empresariais restringem navegadores.

```powershell
cd brand-motion-v27
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
python scripts\doctor.py
```

Em bash, use `source .venv/bin/activate` e `python3` se preciso. Instale FFmpeg separadamente e confirme com `ffmpeg -version`.

## 4 — Testar sem internet (fallback)

```powershell
python scripts\validate_project.py --config examples\demo-saas\manifest.json
python scripts\render_video.py --config examples\demo-saas\manifest.json --output output\demo --preview-only
python scripts\render_video.py --config examples\demo-saas\manifest.json --output output\demo --allow-placeholders
```

O exemplo usa capturas em SVG **fictícias** e não deve ser publicado como demonstração real de uma marca.

## 5 — Produzir para outra marca

Copie `templates/project.example.json` para `meu-video/manifest.json`; copie fotos, screenshots ou logos licenciados para `meu-video/assets/`, atualize as cenas e CTA. Abra os arquivos `SKILL.md`, `references/storyboard.md` e `references/qa-checklist.md`. O agente deve **perguntar nome, site, produto, objetivo e pedir fotos/links de referência** antes de produzir.

**Prática recomendada:** peça ao agente: *“Use a skill brand-motion-v27; quero um vídeo de [minha marca]. Faça o briefing, analise minhas fotos/links e gere storyboard, MP4 e projeto.”*

### Notas

- A referência V27 é uma **metodologia de movimento e enquadramento**, não um asset de terceiros distribuído neste repositório.
- O navegador do projeto genérico usa imagens locais embutidas como `data:` URI, para evitar dependência de acesso externo durante render.
- Cliques em screenshots são **animações sincronizadas**, não interação autenticada com o site; coordenadas devem ser verificadas para corresponder ao elemento real na imagem.
- Os custos de ferramentas externas de imagem/vídeo, música premium ou APIs não estão incluídos; o baseline é local e sem API.
- Música sintetizada original, sem gravações de terceiros. Use faixa externa apenas com licença comprovada.
