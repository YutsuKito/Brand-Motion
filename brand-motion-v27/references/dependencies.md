# Dependências e instalação

## Obrigatórias para gerar MP4 local

- **Python 3.10+** (executa gerador, QA e instalador): https://www.python.org/downloads/
- **FFmpeg e FFprobe** (composição, encode, checagem): https://ffmpeg.org/download.html
- **Playwright para Python** (controle determinístico do navegador): https://playwright.dev/python/docs/intro
- **Chromium** (navegador de renderização, instalado pelo Playwright `python -m playwright install chromium`). Se Chromium estiver bloqueado na empresa, peça autorização/usar navegador existente; não contorne bloqueios.
- **NumPy** (geração de trilha original e SFX) e **Pillow** (storyboard e inspeção).

## Opcionais conforme projeto

- **Git** para clonar repositórios autorizados: https://git-scm.com/downloads
- **Node.js LTS** se for animar frontend real em GSAP/Remotion: https://nodejs.org/en/download
- **GSAP** (motion avançado) https://gsap.com/docs/v3/; **Remotion** (vídeo via React) https://www.remotion.dev/docs; **Three.js** (3D) https://threejs.org/docs/; instale somente se o roteiro precisar.
- **HyperFrames**: apenas quando CLI oficial acessível e confirmada. Esta skill **não depende** do HyperFrames nem finge usar seu CLI.
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
