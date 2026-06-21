import os
from conexao import banco

# PRODUTOS---------------------------------------------------------------------------------------------------------

def buscar_produto(id):
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produto WHERE idProduto = %s"
    dado = (int(id),)
    cursor.execute(comando_SQL, dado)
    busca = cursor.fetchall()

    if busca:
        return 1
    else:
        return 0


def exibir_cardapio():
    # Mostrar o cardapio
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produto"
    cursor.execute(comando_SQL)
    exibir_cardapio = cursor.fetchall()

    if exibir_cardapio:
        print("----- Exibir Cardápio ------")
        for i in range(0, len(exibir_cardapio)):
            print(f"Id da comida: ", exibir_cardapio[i][0])
            print(f"Nome: ", exibir_cardapio[i][1])
            print(f"Preço: ", exibir_cardapio[i][2])
            print(f"Id da categoria: ", exibir_cardapio[i][3])
            print("\n----------------------")


# CATEGORIA---------------------------------------------------------------------------------------------------------

def exibir_categorias():
    cursor = banco.cursor()
    comando_SQL = "SELECT * from categoria"
    cursor.execute(comando_SQL)
    exibir = cursor.fetchall()

    if exibir:
        for i in range(0, len(exibir)):
            print("Nome: ", exibir[i][1])
            print("Id da categoria: ", exibir[i][0])
            print("-----------------------------")


def gerenciar_produto():
    # NOTA: QUERO MUDAR O NOME DISSO!!!!!! Produtos é muito peba, só que COMIDA ou ALIMENTO sinto que não engloba por exemplo as bebidas :/
    print("------ Gerenciar Produtos ------")
    print("[1] - Cadastrar")
    print("[2] - Atualizar")
    print("[3] - Exibir Cardápio")
    print("[4] - Remover")
    escolha = int(input("Escolha a opção desejada: "))
    cursor = banco.cursor()

    os.system('cls' if os.name == 'nt' else 'clear')

    # Cadastrar
    if escolha == 1:
        print("----- Cadastro -----")
        nome = str(input("Informe o nome do produto: "))
        preco = float(input("Informe o preço: R$ "))
        exibir_categorias()
        idCategoria = int(input("Informe o id da categoria: "))

        comando_SQL = "INSERT INTO produto (nome, preco, idCategoria) VALUES (%s, %s, %s)"
        dados = (str(nome), float(preco), int(idCategoria))
        cursor.execute(comando_SQL, dados)
        banco.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Produto cadastrado com sucesso")

    # Atualizar
    elif escolha == 2:
        print("----- Atualizar -----")
        idProd = int(input("Informe o id do produto:"))
        if buscar_produto(idProd) == 1:
            nome = str(input("Informe o nome do produto: "))
            preco = float(input("Informe o preço: R$ "))
            exibir_categorias()
            idCategoria = int(input("Informe o id da categoria: "))

            comando_SQL = "UPDATE produto SET nome = %s, preco = %s, idCategoria = %s WHERE idProduto = %s"
            dados = (str(nome), float(preco), int(idCategoria), int(idProd))
            cursor.execute(comando_SQL, dados)
            banco.commit()

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Produto atualizado com sucesso!")

    elif escolha == 3:
        exibir_cardapio()

    # Remover produto
    elif escolha == 4:
        idProd = int(input("Informe o id do produto:"))
        if buscar_produto(idProd) == 1:
            comando_SQL = "DELETE from produto WHERE idProduto = %s"
            dado = (int(idProd),)
            cursor.execute(comando_SQL, dado)
            banco.commit()

            os.system('cls' if os.name == 'nt' else 'clear')
            print("Produto removido com sucesso!")
    else:
        print("Opção inválida!")
