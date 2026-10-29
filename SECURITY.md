# Segurança e privacidade

## Antes de publicar conteúdo com Brand Motion

- Não inclua `.env`, tokens, chaves privadas, cookies, sessões, capturas de áreas autenticadas ou dados de clientes no repositório ou nos vídeos.
- Use capturas e logos somente com direito de uso. Screenshots demonstrativos são fictícios; não os apresente como resultados reais.
- Não instale Chromium/FFmpeg automaticamente sem autorização em ambientes corporativos.
- Garanta que o agente não publique ou envie dados para serviços externos sem autorização explícita.
- Analise dependências e a origem de assets antes de executar programas de terceiros.

## Escopo da revisão inicial

Revisão de **scripts, HTML, SVGs e documentos**: não foram identificados arquivos `.env`, credenciais, tokens de API, e-mails pessoais, caminhos do usuário ou endereços de rede internos. Código e assets específicos do Aegis Forge foram excluídos deliberadamente. Testes locais de validação do `manifest`, compilação Python e prévia Playwright passaram. Uma auditoria estática não garante ausência de vulnerabilidades em dependências ou futuras contribuições.

Para reportar algo sensível, não publique segredos em issues. Contate o mantenedor de forma privada por um canal disponibilizado no perfil GitHub ou use o mecanismo de reporte privado do GitHub, se habilitado.
