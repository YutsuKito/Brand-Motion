# Analisar e adaptar vídeo de referência

Leia esta referência sempre que o usuário anexar ou indicar um vídeo cujo estilo deseja seguir.

Se o link não puder ser aberto ou o arquivo não estiver acessível, peça que o usuário envie o vídeo ou alguns quadros. Não infira o estilo apenas pelo título ou pela descrição do link.

## Decomposição visual

Antes de criar o storyboard:

1. Verifique duração, proporção, FPS, cortes e trilha com `ffprobe`.
2. Gere uma folha de contato com quadros distribuídos pelo vídeo e quadros adicionais nos cortes e nos pontos de maior movimento. Reveja trechos curtos em velocidade normal para entender timing e causa dos movimentos.
3. Registre em `STYLEBOARD.md` uma descrição objetiva da linguagem visual: paleta, contraste, tipografia ou equivalente aproximado, escala e posição do texto, composição, textura, fotografia, profundidade 3D, formas, grafismos, transições, ritmo, easing, motion blur e tratamento de áudio.
4. Escolha quais características transferir para as fases V27 e onde o elemento Three.js pode pertencer ao estilo sem competir com o produto.

Não copie cada corte mecanicamente. Recrie a hierarquia visual e a gramática do movimento dentro do arco V27, preservando a clareza do produto, do título e do CTA. Quando o vídeo tiver apenas motion 2D, use um detalhe 3D sutil e coerente com suas formas, materiais e ritmo.

## Assets, direitos e proveniência

- Use primeiro arquivos de origem que o usuário fornecer: fotos, screenshots, logo, ilustrações, fontes, modelos 3D, trilha e efeitos sonoros.
- O envio de um vídeo como referência autoriza a análise do estilo; não prova, sozinho, que seus frames, músicas, logos ou outros assets podem ser reutilizados. Se a intenção de reutilizar assets exatos estiver clara mas os direitos não, pergunte brevemente se o usuário tem autorização.
- Reaproveite ou extraia assets exatos somente quando o usuário confirmar que os possui ou pode licenciá-los, ou quando a licença permitir o uso e a distribuição pretendidos. Não remova marcas d'água.
- Sem autorização, crie assets originais que reproduzam características gerais — paleta, silhueta abstrata, geometria, escala, textura e ritmo — sem copiar logotipos, personagens, telas proprietárias, ilustrações identificáveis, slogans ou composições quadro a quadro.
- Registre cada arquivo em `assets-ledger.csv`: nome, origem, licença/autorização, alterações e cenas em que aparece. Registre separadamente os assets criados para substituir elementos da referência.

## Fidelidade do motion

Use a folha de contato para mapear o arco e os keyframes; use análise quadro a quadro para movimentos rápidos. Anote duração de entradas e saídas, pausas de leitura, aceleração, direção, escala, parallax, deformação e transições. Recrie essas curvas com GSAP e calcule a cena Three.js a partir do tempo absoluto recebido pelo seek do HyperFrames. Não use vídeo tocando em tempo real, `requestAnimationFrame`, relógios ou loops independentes.

Compare a prévia com a referência em pontos equivalentes: quadro inicial, início e fim de cada transição, pose de maior energia, hold de leitura e CTA. Corrija primeiro composição, timing, hierarquia e direção do movimento; só depois refine detalhes de textura e luz.

