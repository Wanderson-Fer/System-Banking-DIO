import pandas as pd
from datetime import datetime as dt
from time import sleep
from random import randint


def to_float(valor: str) -> float:
    """
        Função para transformar em 'float',
        com suporte a número REAIS com vírgula,
        validando o valor informado.

        Args:
            valor: valor a ser convertido
        Return:
            retorna o valor passado como argumento convertido para float
    """
    valor = valor.replace(',', '.')  # Formato BR para US
    # Tentando converter, validando com uma exceção.
    try:
        novo_valor = float(valor)
    except ValueError:
        print('Não é um valor numérico.')
        novo_valor = 0

    return novo_valor

def print_title(title: str):
    """Exibição de título, padronizada"""
    print('-'*40)
    print(title.center(40, ' '))
    print('-'*40)

def get_saldo(df: pd.DataFrame) -> float:
    """
        Saldo da conta contido no DataFrame
        Args:
            df: Dataframe com a coluna 'Valor' para as transições
        Returns:
            Saldo da conta obtido através do somatório dos valores
    """
    saldo = df['Valor'].sum()

    return saldo

def get_qtd_saques(df: pd.DataFrame) -> int:
    """
        Quantidade de saques da conta contido no DataFrame
        Args:
            df: Dataframe com a coluna 'Tipo de transação' para as transições 'Saque'
        Returns:
            Quantidade de 'Saques' encontrados no DataFrame
    """

    qtd_linhas, qtd_colunas = df.loc[df['Tipo de transação'] == 'Saque'].shape

    return qtd_linhas

def get_extrato(df: pd.DataFrame, nome: str, conta: str):
    """
        Imprime o extrato a partir do DataFrame com o histórico

        Args:
            df: hitórico de transações com 'Tipo de transação', 'Valor' e 'Data'
            nome: Nome do usuário que realiza a transação
            conta: Numero da conta em que a transação ocorre
    """

    print_title(f'Extrato: {nome} - {conta}')

    # Cabeçalho
    print('Ação'.ljust(12), 'Valor (R$)'.ljust(12), 'Data e Hora'.ljust(18), sep='|')

    # Valores
    for _, registro in df.iterrows():
        print(
            registro['Tipo de transação'].ljust(12),
            f"R$ {registro['Valor']}".ljust(12),
            registro['Data'].strftime('%d/%m/%Y %H:%M:%S').ljust(18),
            sep='|'
        )

    print(f'O saldo final é: {get_saldo(df)}')

def validar_saque(df: pd.DataFrame) -> float:
    """
        Valida o input de saque, caso: seja número, esteja acima do limite, ou do saldo

        Args:
            df: DataFrame com o histórico de transações
        Returns:
            Valor do saque se informado válido
    """

    is_invalid = True
    valor_sacado = 0
    global LIMITE

    while is_invalid:
        valor_sacado = input('>>> R$ ')
        valor_sacado = to_float(valor_sacado)

        if valor_sacado <= 0:
            print('Informe um valor positivo para o saque: ')
        elif valor_sacado > LIMITE:
            print('O valor está acima do limite permitido!')
            print(f'Informe um valor abaido do limite diário de R$ {LIMITE}')
        elif valor_sacado > get_saldo(df):
            print('Saldo insuficiente!')
            if get_saldo(df) > LIMITE:
                print(f'Valor disponível de R$ {LIMITE}')
            else:
                print(f'Valor disponível de R$ {get_saldo(df)}')
        else:
            is_invalid = False

    return - valor_sacado  # Deixando negativo para o df

def sacar(df: pd.DataFrame, nome: str, conta: str) -> pd.DataFrame:
    """
        Operação de saque usando um Dataframe para realizar o registro
        Args:
            df: DataFrame com o histórico de transações
            nome: Nome do usuário que realiza a transação
            conta: Numero da conta em que a transação ocorre
        Return:
            DataFrame com o histórico de transações adicionado da transação, se bem sucedida
    """
    print_title('Sacar')

    print('Informe o valor que deseja sacar: ')
    valor_sacado = validar_saque(df)

    df_nova_trasacao = pd.DataFrame({
        'Usuário': [nome],
        'Número da Conta': [conta],
        'Tipo de transação': ['Saque'],
        'Valor': [valor_sacado],
        'Data': [dt.now()]
    })

    print('Seu saque foi realizado com sucesso!')
    # MOSTRAR NOVO SALDO

    return pd.concat([
        df,
        df_nova_trasacao
    ]).reset_index(drop=True)

def validar_deposito() -> float:
    """
        Valida o input de depósito, caso seja um número positivo

        Returns:
            Valor do depósito se informado válido
    """

    is_invalid = True
    valor_deposito = 0  # Inicializando para evitar problemas de escopo

    while is_invalid:
        valor_deposito = input('>>> R$ ')
        valor_deposito = to_float(valor_deposito)  # Valida se é numérico

        if valor_deposito <= 0:  # Apenas positivo
            print('Informe um valor positivo para o depósito: ')
        else:
            is_invalid = False

    return valor_deposito

def depositar(df: pd.DataFrame, nome: str, conta: str) -> pd.DataFrame:
    """
        Operação de depósito usando um Dataframe para realizar o registro
        Args:
            df: DataFrame com o histórico de transações
            nome: Nome do usuário que realiza a transação
            conta: Numero da conta em que a transação ocorre
        Return:
            DataFrame com o histórico de transações adicionado da transação, se bem sucedida
    """
    print_title('Depositar')

    print('Informe o valor que deseja depositar: ')
    valor_deposito = validar_deposito()

    df_nova_trasacao = pd.DataFrame({
        'Usuário': [nome],
        'Número da Conta': [conta],
        'Tipo de transação': ['Depósito'],
        'Valor': [valor_deposito],
        'Data': [dt.now().strftime('%d/%m/%Y %H:%M:%S')]
    })

    print('Seu depósito foi realizado com sucesso!')
    # MOSTRAR NOVO SALDO

    return pd.concat([
        df,
        df_nova_trasacao
    ]).reset_index(drop=True)

def manipular_conta(df: pd.DataFrame, *, nome: str, conta: str) -> pd.DataFrame:
    """
        Função encapsulada que oferece a interface para realizar
        tranzacões na conta escolhida

        Args:
             df: DataFrame com o histórico de trasações
             nome: Identificação do usuário
             conta: Identificação da conta

        Returns:
            DataFrame acrescido das transações realizadas
    """

    menu_conta = """
        MENU
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [0] Voltar

    >>> """

    # Aplicando filtro no histórico para um único usuário
    df_extrato = df.loc[
        (df['Usuário'] == nome) &
        (df['Número da Conta'] == conta)
    ]

    while True:
        opcao = input(menu_conta)

        if opcao == '0':
            break  # Saíndo do loop e encerrando o programa

        elif opcao == '1':  # Depositar
            # df_extrato = transacao('Depositar', df_extrato)
            df_extrato = depositar(df_extrato, nome, conta)

        elif opcao == '2':  # Sacar
            # contando quantidade de Saques
            qtd_saques_realizados = get_qtd_saques(df_extrato)
            print(f'Saques realizados: {qtd_saques_realizados}')

            if qtd_saques_realizados >= LIMITE_SAQUES:
                print('Quantidade de saques diária atingida!')

            elif get_saldo(df_extrato) <= 0:
                print('Não há saldo na conta para realizar saques!')

            else:
                df_extrato = sacar(df_extrato, nome, conta)

        elif opcao == '3':  # Ver extrato
            if df_extrato.empty:
                print('Nenhuma transação registrada!')
            else:
                get_extrato(df_extrato, nome, conta)

        else:
            print('Ainda estamos trabalhando nisso...')
            print('Escolha uma das opções no menu!')

    print('Voltando ao Menu danterior...')
    sleep(0.5)

    df = pd.concat([
        df,
        df_extrato
    ]).reset_index(drop=True)

    df = df.drop_duplicates()

    return df

def cadastrar_usuario(df: pd.DataFrame) -> pd.DataFrame:
    """
        Realiza o cadastro do usuário

        Args:
            df: DataFrame com os dados de todos os cadastros

        Returns:
            DataFrame acrescido do novo usuário cadastrado
    """

    print_title('Adicionar usuário')

    nome = input('Informe o nome do usuário: ')
    password = input('Informe uma senha para o usuário: ')
    data_cadastro = dt.now().strftime('%d/%m/%Y %H:%M:%S')

    df_novo_usuario = pd.DataFrame({
        'Usuário': [nome],
        'Senha': [password],
        'Data de Cadastro': [data_cadastro]
    })

    print('Usuário adicionado com sucesso!')

    return pd.concat([
        df,
        df_novo_usuario
    ]).reset_index(drop=True)

def selecionar_usuario(df: pd.DataFrame) -> str:
    """
        Interface de seleção de usuários cadastrados

        Args:
            df: DataFrame com as informações dos usuários

        Returns:
            Nome do usuário selecionado
    """

    print('Selecione um usuário')
    for index, users in df.iterrows():
        print(f'[{index}]', users['Usuário'])

    id_selecionado = int(input('>>> '))
    usuario_selecionado = df.loc[id_selecionado, 'Usuário']

    return usuario_selecionado

def cadastrar_conta(df: pd.DataFrame, *, nome: str) -> pd.DataFrame:
    """
        Cadastro de contas para um usuário já existente

        Args:
            df: DataFrame com as informações das contas
            nome: Identificação do usuário que esta realizando o cadastro

        Returns:
            DataFrame acrescido da nova conta cadastrada
    """

    novo_numero_conta = str(randint(100000, 999999))
    # Garantir que seja único
    while novo_numero_conta in list(df['Número da Conta']):
        novo_numero_conta = str(randint(100000, 999999))

    df_nova_conta = pd.DataFrame({
        'Número da Conta': [novo_numero_conta],
        'Usuário': [nome],
        'Data da Criação': [dt.now().strftime('%d/%m/%Y %H:%M:%S')]
    })

    print('Conta')
    print(df_nova_conta.to_string())

    while True:
        foi_confirmado = input('Você deseja confirmar a criação da conta? [Y/n]')

        if foi_confirmado == 'Y':
            print('Conta criada com sucesso!')

            return pd.concat([
                df,
                df_nova_conta
            ])
        elif foi_confirmado == 'n':
            print('Cancelando...')
            # sleep(10)  # para ficar esperto rs
            sleep(1)
            print('A conta não foi criada!')
            return df

def selecionar_conta(df: pd.DataFrame, *, nome: str) -> str:
    """
        Seleciona a conta baseado no cadastro de contas

        Args:
            df: DataFrame com as informações de todas as contas
            nome: Identificação do usuário cuja conta será escolhida

        Returns:
            Identificação da conta selecionada
    """

    print('Selecione uma conta')
    df = df.loc[df['Usuário'] == nome].copy()  # Apenas as contas desse usuário
    for index, users in df.iterrows():
        print(f'[{index}]', users['Usuário'], users['Número da Conta'])

    id_selecionado = int(input('>>> '))
    conta_selecionada = df.loc[id_selecionado, 'Número da Conta']

    return conta_selecionada


if __name__ == '__main__':
    LIMITE = 500.0
    LIMITE_SAQUES = 3

    print_title("Bem-vindo ao DIO Banking!")

    menu_principal = """
            MENU
    [1] Adicionar usuário
    [2] Criar conta-corrente
    [3] Entrar em conta-corrente
    [0] Sair
    
    >>> """

    df_usuarios = pd.DataFrame(columns=['Usuário', 'Senha', 'Data de Cadastro'])
    df_contas = pd.DataFrame(columns=['Número da Conta', 'Usuário', 'Data de Criação'])
    df_historico = pd.DataFrame(columns=['Usuário', 'Número da Conta', 'Tipo de transação', 'Valor', 'Data'])

    while True:
        opcao = input(menu_principal)

        if opcao == '0':
            break
        elif opcao == '1':
            # Adicionar usuário
            df_usuarios = cadastrar_usuario(df_usuarios)

        elif opcao == '2':
            # Abrir conta-corrente vinculada a um usuário
            nome_selecionado = selecionar_usuario(df_usuarios)
            df_contas = cadastrar_conta(df_contas, nome=nome_selecionado)

        elif opcao == '3':
            # Ingressar em conta-corrente
            nome_usuario = selecionar_usuario(df_usuarios)
            numero_conta = selecionar_conta(df_contas, nome=nome_usuario)
            df_historico = manipular_conta(df_historico, nome=nome_usuario, conta=numero_conta)
        else:
            print('Ainda estamos trabalhando nisso...')
            print('Escolha uma das opções no menu!')

    print('\nObrigado por usar nossos serviços!\n')  # Bye
    sleep(1.375)
