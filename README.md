# Atividades Praticas de Processamento de Imagens

Está sendo feito em python, usando as libs que estão em ```requirements.txt```

#### Passos para rodar a aplicação

1. Clonar o repositório
2. Criar um virtualenv no diretório clonado com :
  
      ```python -m venv venv```

      Depois ativar o virtualenv, acho que é assim no windows:

      ```venv\Scripts\activate.bat``` (ou algo similar, realmente não sei como fazer isso no windows)

3. Instalar as dependências no ```requirements.txt```:

    (Eu acho que tem que atualizar o pip)

    ```python -m pip install --upgrade pip```

    ```pip install -r requirements.txt```

4. Pronto 😁, só rodar a ```main.py```

### Coisas para ser implementadas

- [X] Interpolação
  - [X] Por vizinhos próximos (Aumento e diminuição)
  - [X] Bilinear (Aumento e diminuição)
- [ ] Operações aritméticas:
  - [ ] Adição
  - [ ] Subtração
- [X] Operação geométrica:
  - [X] Espelhamento/Reflexão
- [ ] Funções de transformação de intensidade:
  - [X] Negativa
  - [ ] Equalização do histograma normalizado

  


Sendo feito por matheuszinn e thaís apenas.