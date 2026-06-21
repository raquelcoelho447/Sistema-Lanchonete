import os

from cliente import gerenciar_cliente
from funcionario import gerenciar_funcionario
from mesa import gerenciar_mesa
from produto import gerenciar_produto
from pedido import gerenciar_pedido

# Sistema começa aqui
def funcao_principal():
    print(f"Entrando no sistema da Lanchonete")

    while (True):
        # MENU
        print("------------Menu------------")
        print("[1] - Gerenciamento")
        print("[2] - Gerenciar Pedido")
        print("[3] - Gerenciar Mesa")
        print("[4] - Gerenciar Comidas")
        print("[5] - Sair")
        opcao = int(input("Digite a opção desejada: "))

        # Gerenciamento
        if opcao == 1:
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Deseja gerenciar qual das opções: ")
            print("[1] para Cliente")
            print("[2] para Funcionário")
            escolha = int(input("Digite a opção desejada: "))

            # Gerenciar cliente
            if escolha == 1:
                gerenciar_cliente()

            # Gerenciar Funcionario
            elif escolha == 2:
                gerenciar_funcionario()

        # Gerenciar pedido
        elif opcao == 2:
            gerenciar_pedido()

        # Gerenciar mesas
        elif opcao == 3:
            gerenciar_mesa()

        # Gerenciar as Comidas
        elif opcao == 4:
            gerenciar_produto()

        # Sair do sistema
        elif opcao == 5:
            exit()

        # Quando o usuário digita um valor inválido
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opcao inválida! Tente Novamente.")


if __name__ == "__main__":
    funcao_principal()
