# Instrução universal para agentes sem descoberta automática de skills

Leia o arquivo `SKILL.md` desta pasta e aplique o fluxo **Brand Motion V27**. Use HyperFrames, GSAP e Three.js em todo MP4 final. Se o usuário enviar um vídeo de referência, leia `references/style-reference.md`, analise seu estilo e adapte os assets com proveniência e direitos verificados.

**Ao ser acionado sem briefing**, faça uma pergunta direta sobre o produto/marca e o site ou descrição. Depois, conforme o usuário responder, solicite logo, fotos de produtos, capturas de tela ou links de referência; pergunte o objetivo/CTA e onde o vídeo será publicado quando essas informações estiverem ausentes. Não repita respostas já fornecidas. Não comece a renderizar com dados inventados.

Use HyperFrames como único motor do MP4 final. GSAP controla a timeline seekable e Three.js produz pelo menos um elemento 3D coerente com o produto ou vídeo de referência. Python e FFmpeg podem apoiar inspeção e QA, mas não substituir o render final. Se faltar uma dependência, peça consentimento antes de instalar; sem consentimento, explique o bloqueio.

O estilo V27 mantém 4 segundos de explicação com o produto ao lado, 3,5 segundos de zoom com produto centralizado no meio exato do quadro e sem texto, clique/som/troca sincronizados quando houver interface validada e CTA final isolado. Adapte ao vídeo de referência a paleta, composição, tipografia, ritmo, transições e linguagem dos motion graphics. Reuse assets exatos apenas com autorização/licença; sem ela, crie alternativas originais. Não invente telas, ofertas ou promessas.

