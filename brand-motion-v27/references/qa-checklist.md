# QA de produção

1. Verifique origem, permissão e qualidade das imagens e marcas. Liste em `assets-ledger.csv`.
2. Inspecione as cenas quadro a quadro (início, início do zoom, meio do zoom, pré-clique, pós-clique, CTA).
3. Na fase de explicação, a interface deve ficar parada à direita e o texto legível; na fase de foco, ocultar todo o texto e centrar em `width/2,height/2` (tolerância 1 px).
4. Não sobreponha texto à imagem. O quadro de vídeo deve manter todo o conteúdo essencial dentro dos limites; `object-fit: contain` é a opção padrão.
5. Em UI screenshot: clique somente se o `click_target` na screenshot de origem tiver sido validado. A posição normalizada precisa pertencer à região do elemento, não ao fundo. Som e transição visual com offsets da timeline.
6. A ação de navegação e a página exibida devem corresponder. Se isso não puder ser comprovado, omita o click e use corte.
7. O CTA não pode afirmar oferta inexistente. Verificar URL, marca, favicon, acentos, fundo e nuvens atrás do texto.
8. Execute o `qa.py`; use ffprobe e decodificação total via FFmpeg, contagem de frames, canais de áudio e duração. Não diga que o cliente enviou imagem real se não o fez.
9. Entregue resultados efetivamente gerados, não caminhos inventados.
