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

def transacao(tipo: str, df: pd.DataFrame) -> pd.DataFrame:
    """
        Registrar uma transação no 'DataFrame' validando o valor informado.
        Espera-se que a transação já tanha sido permitida.

        Args:
            tipo: Contém informações a respeito da transação
                ('Sacar' ou 'Depositar')
            df: Contém o DataFrame com o histórico de transações
        Return:
            Um DataFrame com o registro da transação
    """
    print(f'{tipo}'.center(30, '-'))

    valor = 0
    print(f'Informe o valor você deseja {tipo}: ')
    while valor <= 0:  # Executando até receber um valor válido
        valor = to_float(input('R$ '))

        if valor <= 0:
            print('Informe um valor válido!')

        if tipo == 'Sacar':
            # Validando limite de valor do saque
            if valor > LIMITE:
                print('Valor informado acima do limite permitido!')
                print(f'O limite é: {LIMITE}')
                print('Informe um valor válido.')
                valor = 0  # Manter dentro do loop

            elif valor > df['Valor'].sum():  # Validando o valor do saque de acordo com o saldo
                print('Saldo insuficiente!')

                if df['Valor'].sum() <= 0.0:
                    print('Você não tem saldo para saques.')
                    return df  # Saindo em caso de saque inviável
                else:
                    valor = 0  # Manter dentro do loop
            else:
                valor = - valor  # Deixando o valor negativo em casos de Saque
                break

    df_nova_trasacao = pd.DataFrame({
        'Tipo de transação': [tipo],
        'Valor': [valor],
        'Data': [dt.now()]
    })

    print('Sua movimentação foi realizada com sucesso!')

    return pd.concat([
        df,
        df_nova_trasacao
    ]).reset_index(drop=True)

def get_extrato(df: pd.DataFrame):
    """
        Imprime o extrato a partir do DataFrame com o histórico

        Args:
            df: hitórico de transações
    """

    print('Extrato'.center(30, '-'))

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

    while True:
        opcao = input(menu)

        if opcao == '0':
            break  # Saíndo do loop e encerrando o programa

        elif opcao == '1':  # Depositar
            df_extrato = transacao('Depositar', df_extrato)

        elif opcao == '2':  # Sacar
            # contando quantidade de Saques
            row, _col = df_extrato.loc[df_extrato['Tipo de transação'] == 'Sacar'].shape
            print(f'Saques realizados: {row}')
            if row >= LIMITE_SAQUES:
                print('Quantidade de saques diária atingida!')
            else:
                df_extrato = transacao('Sacar', df_extrato)

        elif opcao == '3':  # Ver extrato
            if df_extrato.empty:
                print('Nenhuma transação registrada!')
            else:
                get_extrato(df_extrato)

        else:
            print('Ainda estamos trabalhando nisso...')
            print('Escolha uma das opções no menu!')

    print('\nObrigado por usar nossos serviços!\n')  # Bye
    sleep(2)
