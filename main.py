import pandas as pd
from datetime import datetime as dt
from time import sleep


if __name__ == '__main__':
    menu = """
    
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [0] Sair
    
    >>> """

    extrato = pd.DataFrame(columns=['Data', 'Tipo de transação', 'Valor'])
    LIMITE = 500
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu)

        if opcao == '0':
            break

        elif opcao == '1':
            pass

        elif opcao == '2':
            pass

        elif opcao == '3':
            pass

        else:
            print('Ainda estamos trabalhando nisso...')
            print('Escolha uma das opções no menu!')

    print('\nObrigado por usar nossos serviços!\n')
    sleep(3)
