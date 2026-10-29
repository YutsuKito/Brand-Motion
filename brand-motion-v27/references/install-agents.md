# Instalação em agentes

O instalador `scripts/install_skill.py` copia a pasta da skill para o local que cada agente escaneia; não instala o agente em si. Reinicie a sessão ou atualize a lista de skills após instalar.

## Instalação direta do GitHub (recomendada)

Com Node.js 22.20+ instalado, **não é necessário clonar o repositório**.

~~~bash
npx skills add YutsuKito/Brand-Motion --skill brand-motion-v27 -g -a claude-code -a codex -a opencode -a hermes-agent -y
~~~

Alternativa com o endereço direto da pasta:

~~~bash
npx skills add https://github.com/YutsuKito/Brand-Motion/tree/main/brand-motion-v27 --skill brand-motion-v27 -g
~~~

Instalação em apenas um agente:

~~~bash
npx skills add YutsuKito/Brand-Motion --skill brand-motion-v27 -g -a opencode -y
~~~

Para instalar apenas no projeto atual, omita -g. Verifique com npx skills list -g e atualize com npx skills update -g. Hermes Agent na CLI usa a opção hermes-agent (não hermes). Se HERMES_HOME estiver alterado, confira o destino efetivo da instalação.

Este comando não instala HyperFrames, Python, Chromium ou FFmpeg. Consulte dependencies.md e hyperframes.md.

## Instalação manual via script/ZIP

Na pasta onde você extraiu o ZIP (pasta externa ao diretório `brand-motion-v27`):

```bash
python brand-motion-v27/scripts/install_skill.py --agent all --scope user
```

Isso instala em quatro locais separados (sem symlinks, melhor compatibilidade com Windows):

- Codex: `~/.agents/skills/brand-motion-v27/`.
- Claude Code: `~/.claude/skills/brand-motion-v27/`.
- OpenCode: `~/.config/opencode/skills/brand-motion-v27/`.
- Hermes: `~/.hermes/skills/brand-motion-v27/`.

Por projeto:

```bash
python brand-motion-v27/scripts/install_skill.py --agent all --scope project --root /caminho/para/projeto
```

Codex usa `<projeto>/.agents/skills/brand-motion-v27/`, Claude usa `.claude/skills/`, OpenCode usa `.opencode/skills/`; o Hermes, por padrão, continua global em `~/.hermes/skills/` porque esse é seu diretório nativo de skills. Para habilitar em Hermes no projeto, configure diretórios de skills externos no Hermes conforme a documentação da versão instalada.

Pode selecionar apenas um: `--agent codex`, `--agent claude`, `--agent opencode`, ou `--agent hermes`. Use `--dry-run` para inspecionar os destinos. Destinos existentes não são substituídos sem `--replace`. Nenhum arquivo pessoal do agente é modificado fora da pasta específica da skill.

## Acionamento manual depois de instalar

| Agente | Comando recomendado |
| --- | --- |
| OpenCode v2 | `@brand-motion-v27` |
| Codex | `$brand-motion-v27` |
| Claude Code | `/brand-motion-v27` |
| Hermes | `/brand-motion-v27` |

Se a skill não aparecer, reinicie a sessão, confira a instalação e, no OpenCode, confira as permissões da ferramenta `skill`. O caractere `@` é documentado para OpenCode v2, **não** como sintaxe universal.

**Teste de briefing:** acione a skill com `Quero um vídeo da minha marca; antes de produzir, faça as perguntas necessárias e peça imagens ou referências.` O agente deve perguntar ao menos o que é a marca/produto e como obter exemplos visuais, sem renderizar imediatamente.

## Acionamento (alternativo via linguagem natural)

- Codex: selecionar `$brand-motion-v27`, ou pedir um vídeo e deixar o agente escolher a skill.
- Claude Code: usar `/brand-motion-v27` ou pedir uma apresentação de produto.
- OpenCode v2: mencionar `@brand-motion-v27`, ou solicitar a skill `brand-motion-v27` e carregar via ferramenta `skill`.
- Hermes: `/brand-motion-v27` (em sessões que carregaram skills).

Em agentes sem detecção automática, informe o caminho de `SKILL.md` explicitamente ou cole seu conteúdo. Um agente de chat **sem acesso a shell/arquivos** pode ajudar no roteiro, mas não pode garantir MP4 executável.

## Fontes de compatibilidade

- Codex: https://learn.chatgpt.com/docs/build-skills
- Claude: https://platform.claude.com/docs/en/managed-agents/skills e https://code.claude.com/docs
- OpenCode: https://opencode.ai/docs/skills
- Hermes: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Agent Skills: https://agentskills.io
