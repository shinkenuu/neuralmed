### Desafio

Implemente uma API REST que recebe uma imagem e envie a imagem através de uma fila para uma segunda aplicação que a redimensione para o tamanho de 384x384.
Utilize as práticas de programação que achar necessário, levando em consideração que o uso de requisitos e diferenciais listados na vaga será considerado um bônus.
O desenvolvimento deverá ser feito em Python. O projeto deve ser entregue com Docker.

---
##### Extras

 - Se o tamanho for parametrizável como você mudaria a sua arquitetura?
     Exploraria a parametrização por argumentos na requisição (que parece estranho pelo método ser POST. Quanto às mensagens, exploraria passar um JSON com os parametros e os binários da imagem ou linkar a publicação da imagem com seus parametros para que o consumidor receba esses parametros e saiba qual mensagem essa imagem está)
 - Qual a complexidade da sua solução?
 - É possível melhorar a performance da solução? Como as melhorias impactam a leitura e manutenção do código?
  Sim, é super possível. Criar Celery tasks para publicar os eventos e liberar o network IO mais rapidamente, passar os binários das imagens sem escrevê-las em disco, carregar a imagem no Pillow ainda em memória (antes de fazer cache em disco). Se tudo isso ainda não for suficiente, explorar meloria com Profiler.
 - De que forma o sistema pode escalar com a arquitetura planejada?
    Produtores e consumidores podem ser escaladas horizontalmente.

---
##### Observações

O consumidor deve ser adaptados para fazer "acknowledge" de mensagen somente após redimensionar com sucesso ou no caso de X número de falhas para a mesma mensagem.

---

