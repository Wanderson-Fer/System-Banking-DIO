# System Banking DIO with Pandas


![GitHub repo size](https://img.shields.io/github/repo-size/Wanderson-Fer/System-Banking-DIO?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/Wanderson-Fer/System-Banking-DIO?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Wanderson-Fer/System-Banking-DIO?style=for-the-badge)

## Descrição

### Desafio

Fomos contratados por um grande banco para desenvolver o seu novo sistema. Esse banco deseja modernizar as suas operações e para isso escolheu a linguagem Python. Para a primeira versão do sistema devemos implementar apenas 3 operações: depósito, saque e extrato.

- Depósito
    
    Deve ser possível depositar valores positivos para a minha conta bancária. A v1 do projeto trabalha apenas com 1 usuário, dessa forma não precisamos preocupar-nos em identificar qual é o número da agência e conta bancaria. Todos os depósitos devem ser armazenados numa variável e exibidos na operação de extrato.
    
- Saque
    
    O sistema deve permitir realizar 3 saques diários com **limite máximo** de R$ 500,00 por saque. Caso o usuário não tenha saldo em conta, o sistema deve exibir uma mensagem informando que não será possível sacar o dinheiro por **falta de salto**. Todos os saques devem ser armazenados numa variável e exibidos na operação de extrato.
    
- Extrato
    
    Essa operação deve listar todos os depósitos e saques realizados na conta. No fim da listagem deve ser exibido o saldo atual da conta.

#### Uma otimização foi solicitada para adicionar as seguintes funções

- Adicionar usuário

    O sistema deve cadastrar usuários e armazenar essas informações.

- Criar conta-corrente

    O sistema deve cadastrar e armazenar informações de contas.

## Adicionar usuário

![Captura de tela do cadastro de usuário](img/output_screen_add_usuario.png)
> Tela de cadastro de usuário 

## Adicionar conta

![Captura de tela do cadastro de conta](img/output_screen_criar_conta.png)
> Tela de cadastro de conta
 
## Entrar em uma conta

![Captura de tela do ingresso na conta cadastrada](img/output_screen_entrar_conta.png)
> Tela de ingresso na conta cadastrada

## Depósito

![Captura de tela do depósito](img/output_screen_depositar.png)
> Tela de depósito

## Saque

![Captura de tela do saque](img/output_screen_saque.png)
> Tela de saque

## Extrato

![Captura de tela do extrato](img/output_screen_extrato.png)
> Tela de extrato


## 💻 Pré-requisitos

* É necessário ter instalado `Python 3.11`
* Biblioteca `Pandas 2.0.3`, pode ser instalada usando `pip install pandas==2.0.3` 

## Usando o System Banking DIO

Visto que todas as dependências estejam instaladas execute o [main.py](main.py)
ou digite no prompt:

``` PowerShell
    python main.py
```

## Author

### Wanderson G. Fernandes
- [Instagram](https://instagram.com/locke._.wanderson?igshid=ZDc4ODBmNjlmNQ==)
- [LinkedIn](https://www.linkedin.com/in/wanderson-guedes-3138851aa)

## 📝 Licença

Esse projeto está sob licença MIT. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.
