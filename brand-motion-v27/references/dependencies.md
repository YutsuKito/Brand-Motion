# Dependências e instalação

## Obrigatórias para o MP4 final

- **Node.js >=22:** https://nodejs.org/en/download
- **FFmpeg + FFprobe:** https://ffmpeg.org/download.html
- **CLI HyperFrames:** `npx hyperframes`; docs https://hyperframes.app/docs/5-packages/cli
- **GSAP:** timeline pausada e seekable, carregada localmente no projeto: https://gsap.com/docs/v3/
- **Three.js:** módulo local de renderização 3D: https://threejs.org/docs/
- **Python >=3.10:** script export_hyperframes.py para manifest e assets.
- **Diagnóstico:** `npx hyperframes doctor`, depois `npx hyperframes check`, preview e render dentro do projeto.

Para converter um manifest em projeto HyperFrames, veja [hyperframes.md](hyperframes.md). Confirme as dependências com `npx hyperframes doctor` e verifique que GSAP e Three.js estão disponíveis localmente. Não instale dependências sem consentimento do usuário.

## Dependências do renderizador Python legado (não usar para o MP4 final)


- **Python 3.10+** (executa gerador, QA e instalador): https://www.python.org/downloads/
- **FFmpeg e FFprobe** (composição, encode, checagem): https://ffmpeg.org/download.html
- **Playwright para Python** (controle determinístico do navegador): https://playwright.dev/python/docs/intro
- **Chromium** (navegador de renderização, instalado pelo Playwright `python -m playwright install chromium`). Se Chromium estiver bloqueado na empresa, peça autorização/usar navegador existente; não contorne bloqueios.
- **NumPy** (geração de trilha original e SFX) e **Pillow** (storyboard e inspeção).

## Ferramentas auxiliares

- **Git** para clonar repositórios autorizados: https://git-scm.com/downloads
- **Remotion** pode ser usado apenas para inspeção/conversão de projetos antigos; não substitui HyperFrames no MP4 final.
- Geradores de imagens ou vídeo: dependem de serviço, credenciais e direitos de uso específicos; não são exigidos pelo baseline.
- Bancos de música: Mixkit https://mixkit.co/free-stock-music/ ou Pixabay https://pixabay.com/music/; checar licença de cada faixa e plataforma de distribuição. Música original sintetizada localmente não requer download de gravações alheias.

O renderizador Python/Playwright é legado. Pode apoiar QA ou renderizar prévias técnicas, mas nunca gerar o arquivo final desta skill.

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

