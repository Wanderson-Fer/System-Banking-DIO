import pandas as pd
from datetime import datetime as dt
from time import sleep


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

def get_extrato(df: pd.DataFrame):
    """
        Imprime o extrato a partir do DataFrame com o histórico

        Args:
            df: hitórico de transações com 'Tipo de transação', 'Valor' e 'Data'
    """

    print_title('Extrato')

    # Cabeçalho
    print('Ação'.ljust(12), 'Valor (R$)'.ljust(12), 'Data'.ljust(18), sep='|')

    # Valores
    for _, registro in df.iterrows():
        print(
            registro['Tipo de transação'].ljust(12),
            f"R$ {registro['Valor']}".ljust(12),
            registro['Data'].strftime('%d/%m/%Y').ljust(18),
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
            print(f'Informe um valor abaido do limite de R$ {LIMITE}')
        elif valor_sacado > get_saldo(df):
            print('Saldo insuficiente!')
            if get_saldo(df) > LIMITE:
                print(f'Valor disponível de R$ {LIMITE}')
            else:
                print(f'Valor disponível de R$ {get_saldo(df)}')
        else:
            is_invalid = False

    return - valor_sacado  # Deixando negativo para o df

def sacar(df: pd.DataFrame) -> pd.DataFrame:
    """
        Operação de saque usando um Dataframe para realizar o registro
        Args:
            df: DataFrame com o histórico de transações
        Return:
            DataFrame com o histórico de transações adicionado da transação, se bem sucedida
    """
    print_title('Sacar')

    print('Informe o valor que deseja sacar: ')
    valor_sacado = validar_saque(df)

    df_nova_trasacao = pd.DataFrame({
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

def depositar(df: pd.DataFrame) -> pd.DataFrame:
    """
        Operação de depósito usando um Dataframe para realizar o registro
        Args:
            df: DataFrame com o histórico de transações
        Return:
            DataFrame com o histórico de transações adicionado da transação, se bem sucedida
    """
    print_title('Depositar')

    print('Informe o valor que deseja depositar: ')
    valor_deposito = validar_deposito()

    df_nova_trasacao = pd.DataFrame({
        'Tipo de transação': ['Depósito'],
        'Valor': [valor_deposito],
        'Data': [dt.now()]
    })

    print('Seu depósito foi realizado com sucesso!')
    # MOSTRAR NOVO SALDO

    return pd.concat([
        df,
        df_nova_trasacao
    ]).reset_index(drop=True)


if __name__ == '__main__':
    menu = """
    
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [0] Sair
    
    >>> """

    df_extrato = pd.DataFrame(columns=['Tipo de transação', 'Valor', 'Data'])
    LIMITE = 500.0
    LIMITE_SAQUES = 3

    print_title("Bem-vindo ao DIO Banking")
    while True:
        opcao = input(menu)

        if opcao == '0':
            break  # Saíndo do loop e encerrando o programa

        elif opcao == '1':  # Depositar
            # df_extrato = transacao('Depositar', df_extrato)
            df_extrato = depositar(df_extrato)

        elif opcao == '2':  # Sacar
            # contando quantidade de Saques
            qtd_saques_realizados = get_qtd_saques(df_extrato)
            print(f'Saques realizados: {qtd_saques_realizados}')

            if qtd_saques_realizados >= LIMITE_SAQUES:
                print('Quantidade de saques diária atingida!')

            elif get_saldo(df_extrato) <= 0:
                print('Não há saldo na conta para realizar saques!')

            else:
                df_extrato = sacar(df_extrato)

        elif opcao == '3':  # Ver extrato
            if df_extrato.empty:
                print('Nenhuma transação registrada!')
            else:
                get_extrato(df_extrato)

        else:
            print('Ainda estamos trabalhando nisso...')
            print('Escolha uma das opções no menu!')

    print('\nObrigado por usar nossos serviços!\n')  # Bye
    sleep(1.375)
