# Laboratório #2 -- Aprendizado Federado
## Integrantes: Bruno Menegaz, Gustavo Dutra, Leonardo Albergaria
---
## Instruções para Compilação e Execução

> Para realizar a instalação basta clonar o repositório para um diretório local e realizar a instalação do python caso ele não esteja na sua máquina. Também é necessário instalar as bibliotecas tensorflow, flwr e numpy caso não estejam na máquina.

> Em sequência, deve-se iniciar o servidor, alterando no código a variável **num_rounds** para a quantidade desejada. Em Linux, a linha de comando ficará da seguinte forma:

```
$ python3 server.py 
```
> Por fim, devem ser abertos mais 5 terminais, um para cada client.py que será executado. É necessário alterar a variável **cid** no código (e salvar as alterações) antes de executar a linha de comando em cada cliente. O primeiro cliente terá cid = 0, o segundo cid = 1, repetindo até o último cliente com cid = 4.  Em Linux, a linha de comando ficará da seguinte forma:
```
$ python3 client.py 
```

---
## Link para o vídeo no Drive
> https://drive.google.com/file/d/1kNC-liz9AograaGc4B7t5418aDP2DrDF/view?usp=sharing


---
## Implementação, Testes e Conclusões

A implementação completa da primeira atividade e os resultados capturados na segunda foram computados no Colab, a visualização pode ser feita atravez do link:
> https://colab.research.google.com/drive/1bcGdrOwBRgmUJU8Pe2kQGStod6fkJh2Y?usp=sharing#scrollTo=M-zIAMOarmFR

Para as conclusões gerais, podemos destacar que a abordagem federada é capaz de produzir modelos eficientes sem que haja necessidade de se compartilhar os dados com um servidor central, tornando-se assim uma implementação bem interessantes para determinados casos em que a privacidade do cliente é algo fundamental.


