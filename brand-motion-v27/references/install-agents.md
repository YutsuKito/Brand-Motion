# Instalação em agentes

O instalador `scripts/install_skill.py` copia a pasta da skill para o local que cada agente escaneia; não instala o agente em si. Reinicie a sessão ou atualize a lista de skills após instalar.

## Instalação rápida

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

## Acionamento

- Codex: selecionar `$brand-motion-v27`, ou pedir um vídeo e deixar o agente escolher a skill.
- Claude Code: usar `/brand-motion-v27` ou pedir uma apresentação de produto.
- OpenCode: solicitar a skill `brand-motion-v27` e carregar via ferramenta `skill`.
- Hermes: `/brand-motion-v27` (em sessões que carregaram skills).

Em agentes sem detecção automática, informe o caminho de `SKILL.md` explicitamente ou cole seu conteúdo. Um agente de chat **sem acesso a shell/arquivos** pode ajudar no roteiro, mas não pode garantir MP4 executável.

## Fontes de compatibilidade

- Codex: https://learn.chatgpt.com/docs/build-skills
- Claude: https://platform.claude.com/docs/en/managed-agents/skills e https://code.claude.com/docs
- OpenCode: https://opencode.ai/docs/skills
- Hermes: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Agent Skills: https://agentskills.io
