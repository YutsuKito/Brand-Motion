# Dependências e instalação

## Preferenciais para HyperFrames

- **Node.js >=22:** https://nodejs.org/en/download
- **FFmpeg + FFprobe:** https://ffmpeg.org/download.html
- **CLI HyperFrames:** instalar com npm install -g hyperframes; docs https://hyperframes.app/docs/5-packages/cli
- **Skills oficiais:** npx skills add heygen-com/hyperframes (instalação requer aprovação)
- **Python >=3.10:** script export_hyperframes.py para manifest e assets.
- **Diagnóstico:** npx hyperframes doctor, depois npx hyperframes lint/render dentro do projeto.

Para converter um manifest em projeto HyperFrames, veja [hyperframes.md](hyperframes.md). O CLI 0.8.217 passou doctor, lint, preview e render no teste local isolado; confirme as dependências com `npx hyperframes doctor` na máquina de produção.

## Obrigatórias somente para o fallback Python


- **Python 3.10+** (executa gerador, QA e instalador): https://www.python.org/downloads/
- **FFmpeg e FFprobe** (composição, encode, checagem): https://ffmpeg.org/download.html
- **Playwright para Python** (controle determinístico do navegador): https://playwright.dev/python/docs/intro
- **Chromium** (navegador de renderização, instalado pelo Playwright `python -m playwright install chromium`). Se Chromium estiver bloqueado na empresa, peça autorização/usar navegador existente; não contorne bloqueios.
- **NumPy** (geração de trilha original e SFX) e **Pillow** (storyboard e inspeção).

## Opcionais conforme projeto

- **Git** para clonar repositórios autorizados: https://git-scm.com/downloads
- **Node.js LTS** se for animar frontend real em GSAP/Remotion: https://nodejs.org/en/download
- **GSAP** (motion avançado) https://gsap.com/docs/v3/; **Remotion** (vídeo via React) https://www.remotion.dev/docs; **Three.js** (3D) https://threejs.org/docs/; instale somente se o roteiro precisar.
- **HyperFrames** é preferencial para novas produções (veja a seção acima); o motor Python é alternativa, não a implementação do HyperFrames.
- Geradores de imagens ou vídeo: dependem de serviço, credenciais e direitos de uso específicos; não são exigidos pelo baseline.
- Bancos de música: Mixkit https://mixkit.co/free-stock-music/ ou Pixabay https://pixabay.com/music/; checar licença de cada faixa e plataforma de distribuição. Música original sintetizada localmente não requer download de gravações alheias.

## Instalar dependências Python

Na pasta do skill (preferencialmente usando venv):

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python scripts/doctor.py
```

Se o navegador falhar no Linux por dependências do SO, leia os avisos de `playwright install` e peça permissão para instalar pacotes. Não execute `sudo` automaticamente. FFmpeg precisa estar no `PATH`.

**Não instale o agente de IA com estes comandos.** Eles instalam exclusivamente as dependências de produção. Cada agente (Claude, Codex, etc.) tem seu próprio instalador e autenticação; a skill é independente disso.
