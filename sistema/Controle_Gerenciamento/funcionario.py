import os
from conexao import banco

# FUNCIONARIO---------------------------------------------------------------------------------------------------------

def gerenciar_funcionario():
    print("--- Gerenciamento de Funcionários ---")
    print("[1] - Cadastrar")
    print("[2] - Buscar")
    print("[3] - Atualizar")
    print("[4] - Excluir")
    print("[5] - Voltar")
    opcao = int(input("Digite a opção desejada: "))

    cursor = banco.cursor()

    # Cadastrar funcionário
    if opcao == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        salario = float(input("Digite o salário: R$ "))
        cpf = str(input("Digite o CPF: "))
        nome = str(input("Digite o nome: "))
        funcao = str(input("Digite a função: "))

        comando_SQL = "INSERT INTO funcionario (salario, cpf, nome, funcao) VALUES (%s, %s, %s, %s)"
        dados = (float(salario), str(cpf), str(nome), str(funcao))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Funcionário cadastrado com sucesso!")

    # Buscar Funcionário
    elif opcao == 2:
        cpf = str(input("Informe o CPF: "))
        comando_SQL = "SELECT * from funcionario WHERE cpf = %s"
        dado = (str(cpf),)
        cursor.execute(comando_SQL, dado)
        busca = cursor.fetchall()

        os.system('cls' if os.name == 'nt' else 'clear')

        print("--- Informações do Funcionário ---")
        for i in range(0, len(busca)):
            if busca[i][2] == cpf:
                print(f"Nome: ", busca[i][3])
                print(f"Código do Funcionário: ", busca[i][0])
                print(f"CPF: ", busca[i][2])
                print(f"Salário: ", busca[i][1])
                print(f"Função: ", busca[i][4])
                print("-------------------------------")

    # Atualizar dados do funcionário
    elif opcao == 3:
        cpf = str(input("Informe o CPF: "))
        comando_SQL = "SELECT * from funcionario WHERE cpf = %s"
        dado = (str(cpf),)
        cursor.execute(comando_SQL, dado)
        busca = cursor.fetchall()

        os.system('cls' if os.name == 'nt' else 'clear')

        if busca:
            print("--- Atualizar Informações ---")
            salario = float(input("Salário: R$ "))
            cpf = str(input("CPF: "))
            nome = str(input("Nome: "))
            funcao = str(input("Função: "))
            idFunc = busca[0][0]

            comando_SQL = "UPDATE funcionario SET salario = %s, cpf = %s, nome = %s, funcao = %s WHERE idFunc = %s"
            dados = (float(salario), str(cpf), str(nome), str(funcao), int(idFunc))
            cursor.execute(comando_SQL, dados)
            banco.commit()

    # Excluir funcionário
    elif opcao == 4:
        cpf = str(input("Informe o CPF: "))
        comando_SQL = "DELETE from funcionario WHERE cpf = %s"
        dado = (str(cpf),)
        cursor.execute(comando_SQL, dado)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Funcionário removido com sucesso!")

    # Voltar para o MENU principal
    elif opcao == 5:
        return "voltar"
