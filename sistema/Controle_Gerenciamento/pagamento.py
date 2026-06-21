import os
from conexao import banco

# PAGAMENTO---------------------------------------------------------------------------------------------------------

def imprimir_nota_fiscal():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM pagamento"
    cursor.execute(comando_SQL)
    imprimir_nota_fiscal = cursor.fetchall()

    os.system('cls' if os.name == 'nt' else 'clear')

    if imprimir_nota_fiscal:
        print("---- Nota Fiscal ----")
        for i in range(0, len(imprimir_nota_fiscal)):
            print("ID do pagamento: ", imprimir_nota_fiscal[i][0])
            print("Forma de pagamento: ", imprimir_nota_fiscal[i][1])
            print("Valor: R$", imprimir_nota_fiscal[i][2])
            print("ID do pedido: ", imprimir_nota_fiscal[i][3])
            print("----------------------------------------------")


def nota_fiscal(id):
    from pedido import listar_pedidos_cliente

    # Adicionando todas as comidas que o cliente irá pagar na tabela PAGAMENTO
    cursor = banco.cursor()
    listar_pedidos_cliente(id)
    print("------ Pagamento ------")
    idPedido = int(input("Selecione o pedido: "))

    comando_SQL = "SELECT total, idMesa from pedido WHERE idPedido = %s"
    dado = (int(idPedido),)
    cursor.execute(comando_SQL, dado)
    precos = cursor.fetchall()

    # aqui tá acontecendo o seguinte: quando passar o id do pedido, o valor do pedido e o ID será adicionado na tabela pagamento
    if precos:
        comando_SQL = "INSERT INTO pagamento (valor, idPedido) VALUES (%s, %s)"
        dados = (float(precos[0][0]), int(idPedido),)
        cursor.execute(comando_SQL, dados)
        banco.commit()

        # Liberar a mesa do pedido pago
        idMesa = precos[0][1]
        comando_SQL = "UPDATE mesa SET status = 'Disponível' WHERE idMesa = %s"
        cursor.execute(comando_SQL, (int(idMesa),))
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Pagamento realizado com sucesso! Mesa liberada.")
