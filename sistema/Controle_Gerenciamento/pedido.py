import os
from conexao import banco

# PEDIDOS---------------------------------------------------------------------------------------------------------

def fazer_pedido(data, valor, idCli, idFunc, idMesa, idProd):
    # Aqui basicamente é o processo de fazer um pedido
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO pedido (data, total, idCliente, idFunc, idMesa, idProduto) VALUES (%s, %s, %s, %s, %s, %s)"
    dados = (str(data), float(valor), int(idCli), int(idFunc), int(idMesa), int(idProd))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    # TO COM PREGUIÇA DE COMENTAR O QUE É ISSO AQUI
    qtd = int(input("Quantidade: "))
    comando_SQL = "SELECT preco FROM produto WHERE idProduto = %s"
    cursor.execute(comando_SQL, (int(idProd),))
    busca = cursor.fetchall()

    if qtd == 1:
        subTotal = busca[0][0]
    elif qtd > 1:
        subTotal = (busca[0][0]) * qtd

    comando_SQL = "SELECT idPedido, idProduto, idCliente, data FROM pedido"
    cursor.execute(comando_SQL)
    busca = cursor.fetchall()

    if busca:
        for i in range(0, len(busca)):
            print(f"Id do Pedido: ", busca[i][0])
            print(f"Id do Produto: ", busca[i][1])
            print(f"Id do Cliente: ", busca[i][2])
            print(f"Data: ", busca[i][3])
            print("----------------------------------")

    idPedido = int(input("Informe o id do pedido: "))
    comando_SQL = "INSERT INTO itemPedido (subtotal, quantidade, idPedido, idProduto) VALUES (%s, %s, %s, %s)"
    dados = (float(subTotal), int(qtd), int(idPedido), int(idProd))
    cursor.execute(comando_SQL, dados)
    banco.commit()


def buscar_pedidos_cliente(id):
    contador = 0
    cursor = banco.cursor()
    comando_SQL = "SELECT pedido.idPedido, produto.nome FROM pedido INNER JOIN produto ON pedido.idProduto = produto.idProduto WHERE pedido.idCliente = %s"
    dado = (int(id),)
    cursor.execute(comando_SQL, dado)
    buscar_pedidos_de_um_cliente = cursor.fetchall()

    if buscar_pedidos_de_um_cliente:
        for i in range(0, len(buscar_pedidos_de_um_cliente)):
            print("Nome: ", buscar_pedidos_de_um_cliente[i][1])
            print("Pedido: ", buscar_pedidos_de_um_cliente[i][0])
            print("----------------------------------------")
            contador += 1

    return contador


def listar_pedidos_cliente(id):
    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido WHERE idCliente = %s"
    dado = (int(id),)
    cursor.execute(comando_SQL, dado)
    listar_pedidos_de_um_cliente = cursor.fetchall()

    if listar_pedidos_de_um_cliente:
        comando_SQL = "SELECT nome FROM cliente WHERE idCliente = %s"
        dado = (int(id),)
        cursor.execute(comando_SQL, dado)
        nomeCliente = cursor.fetchall()

        print("Nota fiscal do cliente - ", nomeCliente[0][0])
        for i in range(0, len(listar_pedidos_de_um_cliente)):
            print(f"Id do pedido: ", listar_pedidos_de_um_cliente[i][0])
            print(f"Data do pedido: ", listar_pedidos_de_um_cliente[i][1])
            print(f"Valor: R$", listar_pedidos_de_um_cliente[i][2])
            print(f"Id do Cliente: ", listar_pedidos_de_um_cliente[i][3])
            print(f"Id do Funcionário: ", listar_pedidos_de_um_cliente[i][4])
            print(f"Id da Mesa: ", listar_pedidos_de_um_cliente[i][5])
            print(f"Id da Comida: ", listar_pedidos_de_um_cliente[i][6])
            print("-------------------------------------")


def buscar_pedido(id):
    # Buscar um pedido passando como parâmetro o ID
    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido WHERE idPedido = %s"
    dado = (int(id),)
    cursor.execute(comando_SQL, dado)
    busca = cursor.fetchall()

    if busca:
        return id
    else:
        print("Nenhum pedido foi encontrado!")
        return 0


def listar_pedidos():
    # Mostrar todos os pedidos cadastrados
    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido"
    cursor.execute(comando_SQL)
    busca = cursor.fetchall()

    if busca:
        os.system('cls' if os.name == 'nt' else 'clear')

        for i in range(0, len(busca)):
            print(f"Id do pedido: ", busca[i][0])
            print(f"Data do pedido: ", busca[i][1])
            print(f"Valor: R$", busca[i][2])
            print(f"Id do Cliente: ", busca[i][3])
            print(f"Id do Funcionário: ", busca[i][4])
            print(f"Id da Mesa: ", busca[i][5])
            print(f"Id da Comida: ", busca[i][6])


def gerenciar_pedido():
    from mesa import reservar_mesa
    from produto import exibir_cardapio
    from pagamento import nota_fiscal, imprimir_nota_fiscal

    print("Escolha uma opção: ")
    print("[1] - Fazer pedido")
    print("[2] - Remover pedido")
    print("[3] - Atualizar pedido")
    print("[4] - Listar pedidos")
    print("[5] - Realizar Pagamento")
    print("[6] - Voltar")
    escolha = int(input("Escolha a opção desejada: "))
    cursor = banco.cursor()

    # Opção para fazer o pedido
    if escolha == 1:
        print("-------- Fazer Pedido --------")
        cpfCli = str(input("Informe o CPF do cliente: "))
        cpfFunc = str(input("Informe o CPF do funcionário: "))

        cursor = banco.cursor()
        comando_SQL = "SELECT idCliente FROM cliente WHERE cpf = %s"
        cursor.execute(comando_SQL, (cpfCli,))
        cliente_encontrado = cursor.fetchall()

        comando_SQL = "SELECT idFunc FROM funcionario WHERE cpf = %s"
        cursor.execute(comando_SQL, (cpfFunc,))
        funcionario_encontrado = cursor.fetchall()

        busca = [(cliente_encontrado[0][0], funcionario_encontrado[0][0])] if cliente_encontrado and funcionario_encontrado else []

        # aqui significa que a busca teve sucesso em encontrar tanto o cliente e funcionário buscado
        if busca:
            resultado_reserva = reservar_mesa()
            if resultado_reserva != 0:

                os.system('cls' if os.name == 'nt' else 'clear')

                # Mostrar as comidas que tem
                exibir_cardapio()

                # Para fazer o pedido, precisa preencher esses atributos:
                data = str(input("Data: "))
                pedido = int(input("PEDIDO (insira o id): "))

                # pegar o preço da comida
                comando_SQL = "SELECT preco from produto WHERE idProduto = %s"
                dado = (int(pedido),)
                cursor.execute(comando_SQL, dado)
                valor = cursor.fetchall()

                if valor:
                    fazer_pedido(data, valor, busca[0][0], busca[0][1], resultado_reserva, pedido)

                os.system('cls' if os.name == 'nt' else 'clear')
                print("Pedido feito com sucesso!")
        else:
            if not cliente_encontrado:
                print("Cliente não encontrado! Verifique o CPF informado.")
            if not funcionario_encontrado:
                print("Funcionário não encontrado! Verifique o CPF informado.")
            input("Pressione Enter para voltar ao menu...")

    # Opção para remover o pedido
    elif escolha == 2:
        idPedido = int(input("Informe o id do pedido: "))

        comando_SQL = "DELETE from pedido WHERE idPedido = %s"
        dado = (int(idPedido),)
        cursor.execute(comando_SQL, dado)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Pedido removido com sucesso!")

    # Opção para atualizar pedido
    elif escolha == 3:
        data = str(input("Data: "))
        valor = float(input("Valor: R$"))
        idCli = int(input("Id do Cliente: "))
        idFunc = int(input("Id do Funcionário: "))
        idMesa = int(input("Id do Mesa: "))
        idProduto = int(input("Id do Produto: "))
        idPedido = int(input("Informe o id do pedido: "))
        res_idPedido = buscar_pedido(idPedido)

        comando_SQL = "UPDATE pedido SET data = %s, total = %s, idCliente = %s, idFunc = %s, idMesa = %s, idProduto = %s WHERE idPedido = %s"
        dados = (str(data), float(valor), int(idCli), int(idFunc), int(idMesa), int(idProduto), int(res_idPedido))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Pedido atualizado com sucesso!")

    # Listar todos os pedidos
    elif escolha == 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        listar_pedidos()

    # Fazer o pagamento
    elif escolha == 5:
        idCliPagamento = int(input("Informe o id do cliente: "))
        nota_fiscal(idCliPagamento)
        imprimir_nota_fiscal()

    # Opção voltar
    elif escolha == 6:
        return "voltar"

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Opção inválida!")