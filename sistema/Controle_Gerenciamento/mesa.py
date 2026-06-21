import os
from conexao import banco

# MESA---------------------------------------------------------------------------------------------------------

def buscar_mesa(numero):
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa WHERE numero = %s"
    dado = (int(numero),)
    cursor.execute(comando_SQL, dado)
    busca = cursor.fetchall()

    if busca:
        return busca
    else:
        return 0


def listar_mesas():
    # Serve para mostrar TODAS as mesas cadastradas no sistema
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    # Exibir as mesas
    if exibir_mesas:
        print("------- Listagem de Mesas -------")
        for i in range(0, len(exibir_mesas)):
            print(f"Id da mesa: ", exibir_mesas[i][0])
            print(f"Status: ", exibir_mesas[i][1])
            print(f"Numero: ", exibir_mesas[i][2])
            print(f"Capacidade: ", exibir_mesas[i][3])
            print("-------------------------")


def reservar_mesa():
    # Verificar no BD as mesas que tem disponivel
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa WHERE status = 'Disponível'"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    # Exibir as mesas
    if exibir_mesas:
        print("------- Mesas Disponíveis -------")
        for i in range(0, len(exibir_mesas)):
            print(f"Id da mesa: ", exibir_mesas[i][0])
            print(f"Status: ", exibir_mesas[i][1])
            print(f"Numero: ", exibir_mesas[i][2])
            print(f"Capacidade: ", exibir_mesas[i][3])
            print("-------------------------")

        reserva = int(input("Informe o id da mesa que será reservada: "))
        comando_SQL = "UPDATE mesa SET status = 'Ocupada' WHERE idMesa = %s"
        dado = (int(reserva),)
        cursor.execute(comando_SQL, dado)
        banco.commit()
        return reserva
    else:
        print("Não há nenhuma mesa cadastrada!")
        return 0


def gerenciar_mesa():
    print("Escolha uma opção: ")
    print("[1] - Cadastrar")
    print("[2] - Remover")
    print("[3] - Listar")
    escolha = int(input("Escolha a opção desejada: "))
    cursor = banco.cursor()

    # Opção para cadastrar a mesa
    if escolha == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("---- Cadastro de mesas ----")

        status = "Disponível"
        numero = int(input("Informe o número da mesa: "))
        capacidade = int(input("Informe a capacidade: "))
        comando_SQL = "INSERT INTO mesa (status, numero, capacidade) VALUES (%s, %s, %s)"
        dados = (str(status), int(numero), int(capacidade))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        print("Mesa cadastrada com sucesso!")

    # Opção para remover a mesa
    elif escolha == 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("---- Remover mesa ----")

        numero = int(input("Informe o numero da mesa: "))
        if buscar_mesa(numero):
            comando_SQL = "DELETE from mesa WHERE numero = %s"
            dado = (int(numero),)
            cursor.execute(comando_SQL, dado)
            banco.commit()

    # Opção para listar todas as mesas cadastradas
    elif escolha == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        listar_mesas()

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Opção inválida!")
