import os
from conexao import banco

# CLIENTE---------------------------------------------------------------------------------------------------------

def buscar_cliente(cpf):
    cursor = banco.cursor()
    comando_SQL = "SELECT idCliente from cliente WHERE cpf = %s"
    dado = (str(cpf),)
    cursor.execute(comando_SQL, dado)
    busca = cursor.fetchall()

    if busca:
        return busca
    else:
        print("Nenhum cliente foi encontrado")
        return 0


def gerenciar_cliente():
    print("--- Gerenciamento de Clientes ---")
    print("[1] - Cadastrar")
    print("[2] - Buscar")
    print("[3] - Atualizar")
    print("[4] - Excluir")
    print("[5] - Voltar")
    opcao = int(input("Digite a opção desejada: "))

    cursor = banco.cursor()
    os.system('cls' if os.name == 'nt' else 'clear')

    # Cadastrar cliente
    if opcao == 1:
        nome = str(input("Digite o nome: "))
        cpf = str(input("Digite o CPF: "))
        telefone = str(input("Digite o número (formato: (XX) XXXXX-XXXX): "))

        comando_SQL = "INSERT INTO cliente (telefone, cpf, nome) VALUES (%s, %s, %s)"
        dados = (str(telefone), str(cpf), str(nome))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Cliente cadastrado com sucesso!")

    # Buscar Cliente
    elif opcao == 2:
        cpf = str(input("Informe o CPF: "))
        comando_SQL = "SELECT * from cliente WHERE cpf = %s"
        dado = (str(cpf),)
        cursor.execute(comando_SQL, dado)
        busca = cursor.fetchall()

        os.system('cls' if os.name == 'nt' else 'clear')

        print("--- Informações do Cliente ---")
        for i in range(0, len(busca)):
            if busca[i][2] == cpf:
                print(f"Nome: ", busca[i][3])
                print(f"Código do CLiente: ", busca[i][0])
                print(f"CPF: ", busca[i][2])
                print(f"Telefone: ", busca[i][1])
                print("-------------------------------")

    # Atualizar dados do cliente
    elif opcao == 3:
        cpf = str(input("Informe o CPF: "))
        comando_SQL = "SELECT * from cliente WHERE cpf = %s"
        dado = (str(cpf),)
        cursor.execute(comando_SQL, dado)
        busca = cursor.fetchall()

        os.system('cls' if os.name == 'nt' else 'clear')

        if busca:
            print("--- Atualizar Informações ---")
            telefone = str(input("Telefone: "))
            cpf = str(input("CPF: "))
            nome = str(input("Nome: "))
            idCli = busca[0][0]

            comando_SQL = "UPDATE cliente SET telefone = %s, cpf = %s, nome = %s WHERE idCliente = %s"
            dados = (str(telefone), str(cpf), str(nome), str(idCli))
            cursor.execute(comando_SQL, dados)
            banco.commit()

    # Excluir cliente
    elif opcao == 4:
        cpf = str(input("Informe o CPF: "))
        comando_SQL = "DELETE from cliente WHERE cpf = %s"
        dado = (str(cpf),)
        cursor.execute(comando_SQL, dado)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Cliente removido com sucesso!")

    # Voltar para o MENU principal
    elif opcao == 5:
        return "voltar"
