from pathlib import Path
import mysql.connector
from PyQt5 import uic, QtWidgets

numero_idFunc = 0
numero_idPedido = 0
numero_idMesa = 0
numero_idCliente = 0
idCli_res = 0
idFunc_res = 0
numero_idComida = 0

# Variáveis para o fluxo de fazer pedido
numero_idCliente_pedido = 0   # ID do cliente validado
numero_idFunc_pedido = 0      # ID do funcionário validado
carrinho = []                 # lista de dicts: {idProduto, nome, preco, quantidade, subTotal}

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Rachel1307.",
    database="lanchonete"
)

# Clientes -------------------------------------------------------------------------------------------------------
def gerenciarClientes():
    telaPrincipal.close()
    telaClientes.show()
    listarClientes()


def listarClientes():
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente")
    busca = cursor.fetchall()

    telaClientes.tabela_clientes.setRowCount(len(busca))
    telaClientes.tabela_clientes.setColumnCount(4)

    for i in range(len(busca)):
        for j in range(4):
            telaClientes.tabela_clientes.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def cadastrarCliente():
    telaClientes.close()
    telaClientes_cadastro.show()


def confirmarCadastro_cliente():
    nome     = telaClientes_cadastro.txt_nomeCadastroCliente.text()
    cpf      = telaClientes_cadastro.txt_cpfCadastroCliente.text()
    telefone = telaClientes_cadastro.txt_telefoneCadastroCliente.text()

    cursor = banco.cursor()
    cursor.execute(
        "INSERT INTO cliente (telefone, cpf, nome) VALUES (%s, %s, %s)",
        (str(telefone), str(cpf), str(nome))
    )
    banco.commit()

    telaClientes_cadastro.close()
    atualizarTabelaClientes()


def buscarCliente():
    id = telaClientes.txt_buscarCliente.text()

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente WHERE idCliente = %s", (int(id),))
    busca = cursor.fetchall()

    telaClientes.tabela_clientes.setRowCount(len(busca))
    telaClientes.tabela_clientes.setColumnCount(4)

    for i in range(len(busca)):
        for j in range(4):
            telaClientes.tabela_clientes.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def atualizarCliente():
    global numero_idCliente
    linha = telaClientes.tabela_clientes.currentRow()

    if linha == -1:
        QtWidgets.QMessageBox.warning(None, "Nenhum cliente selecionado", "Selecione um cliente antes de atualizar.")
        return

    valor_id = int(telaClientes.tabela_clientes.item(linha, 0).text())

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente WHERE idCliente = %s", (valor_id,))
    cliente = cursor.fetchone()

    if not cliente:
        return

    numero_idCliente = valor_id

    telaClientes_atualizar.txt_idAtualizarCliente.setText(str(cliente[0]))
    telaClientes_atualizar.txt_telefoneAtualizarCliente.setText(str(cliente[1]))
    telaClientes_atualizar.txt_cpfAtualizarCliente.setText(str(cliente[2]))
    telaClientes_atualizar.txt_nomeAtualizarCliente.setText(str(cliente[3]))

    telaClientes.close()
    telaClientes_atualizar.show()


def salvarCliente():
    global numero_idCliente
    nome     = telaClientes_atualizar.txt_nomeAtualizarCliente.text()
    cpf      = telaClientes_atualizar.txt_cpfAtualizarCliente.text()
    telefone = telaClientes_atualizar.txt_telefoneAtualizarCliente.text()

    cursor = banco.cursor()
    cursor.execute(
        "UPDATE cliente SET nome = %s, cpf = %s, telefone = %s WHERE idCliente = %s",
        (str(nome), str(cpf), str(telefone), int(numero_idCliente))
    )
    banco.commit()

    telaClientes_atualizar.close()
    atualizarTabelaClientes()


def removerCliente():
    linha = telaClientes.tabela_clientes.currentRow()

    if linha == -1:
        QtWidgets.QMessageBox.warning(None, "Nenhum cliente selecionado", "Selecione um cliente antes de remover.")
        return

    valor_id = int(telaClientes.tabela_clientes.item(linha, 0).text())

    cursor = banco.cursor()
    cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (valor_id,))
    banco.commit()

    atualizarTabelaClientes()


def atualizarTabelaClientes():
    telaClientes.show()

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente")
    dados_lidos = cursor.fetchall()

    telaClientes.tabela_clientes.setRowCount(len(dados_lidos))
    telaClientes.tabela_clientes.setColumnCount(4)

    for i in range(len(dados_lidos)):
        for j in range(4):
            telaClientes.tabela_clientes.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

# Funcionários -------------------------------------------------------------------------------------------------------
def gerenciarFunc():
    telaPrincipal.close()
    telaFunc.show()


def cadastrarFunc():
    telaFunc.close()
    telaFunc_cadastro.show()


def confirmarCadastro_func():
    nome = telaFunc_cadastro.txt_nomeCadastroFunc.text()
    cpf = telaFunc_cadastro.txt_cpfCadastroFunc.text()
    salario = telaFunc_cadastro.txt_salarioCadastroFunc.text()
    funcao = telaFunc_cadastro.txt_funcaoCadastroFunc.text()

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO funcionario (salario, cpf, nome, funcao) VALUES (%s, %s, %s, %s)"
    dados = (float(salario), str(cpf), str(nome), str(funcao))
    cursor.execute(comando_SQL, dados)
    banco.commit()
    telaFunc_cadastro.close()
    atualizarTabelaFunc()


def buscarFunc():
    id = telaFunc.txt_buscarFunc.text()

    cursor = banco.cursor()
    comando_SQL = "SELECT * from funcionario WHERE idFunc = %s"
    dado = (int(id),)
    cursor.execute(comando_SQL, dado)
    busca = cursor.fetchall()

    telaFunc.tabela_funcionarios.setRowCount(len(busca))
    telaFunc.tabela_funcionarios.setColumnCount(4)

    for i in range(0, len(busca)):
         for j in range(0, 4):
            telaFunc.tabela_funcionarios.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def listarFuncionarios():
    cursor = banco.cursor()
    comando_SQL = "SELECT * from funcionario"
    cursor.execute(comando_SQL)
    busca = cursor.fetchall()

    telaFunc.tabela_funcionarios.setRowCount(len(busca))
    telaFunc.tabela_funcionarios.setColumnCount(5)

    for i in range(0, len(busca)):
         for j in range(0, 5):
            telaFunc.tabela_funcionarios.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def atualizarFunc():
    global numero_idFunc
    linha = telaFunc.tabela_funcionarios.currentRow()

    if linha == -1:
        QtWidgets.QMessageBox.warning(None, "Nenhum funcionário selecionado", "Selecione um funcionário antes de atualizar.")
        return

    valor_id = int(telaFunc.tabela_funcionarios.item(linha, 0).text())

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM funcionario WHERE idFunc = %s"
    dado = (valor_id,)
    cursor.execute(comando_SQL, dado)
    func = cursor.fetchone()

    if not func:
        return

    telaFunc_atualizar.show()

    numero_idFunc = valor_id

    telaFunc_atualizar.txt_nomeAtualizarFunc.setText(str(func[3]))
    telaFunc_atualizar.txt_salarioAtualizarFunc.setText(str(func[1]))
    telaFunc_atualizar.txt_funcaoAtualizarFunc.setText(str(func[4]))


def salvarFuncionario():
    # pega o numero do id
    global numero_idFunc
    nome = telaFunc_atualizar.txt_nomeAtualizarFunc.text()
    salario = telaFunc_atualizar.txt_salarioAtualizarFunc.text()
    funcao = telaFunc_atualizar.txt_funcaoAtualizarFunc.text()

    cursor = banco.cursor()
    comando_SQL = "UPDATE funcionario SET nome = %s, salario = %s, funcao = %s WHERE idFunc = %s"
    dados_lidos = (str(nome), float(salario), str(funcao), int(numero_idFunc))
    cursor.execute(comando_SQL, dados_lidos)
    banco.commit()

    # atualizar as janelas
    telaFunc_atualizar.close()
    telaFunc.close()
    atualizarTabelaFunc()


def removerFuncionario():
    linha = telaFunc.tabela_funcionarios.currentRow()

    if linha == -1:
        QtWidgets.QMessageBox.warning(None, "Nenhum funcionário selecionado", "Selecione um funcionário antes de remover.")
        return

    valor_id = int(telaFunc.tabela_funcionarios.item(linha, 0).text())

    cursor = banco.cursor()
    cursor.execute("DELETE FROM funcionario WHERE idFunc = %s", (valor_id,))
    banco.commit()

    atualizarTabelaFunc()


def atualizarTabelaFunc():
    telaFunc.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM funcionario"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaFunc.tabela_funcionarios.setRowCount(len(dados_lidos))
    telaFunc.tabela_funcionarios.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
         for j in range(0, 5):
            telaFunc.tabela_funcionarios.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# Pedidos -------------------------------------------------------------------------------------------------------
def gerenciarPedidos():
    telaPrincipal.close()
    telaPedidos.show()
    atualizarTotalPedidos()


def abrirTelaValidacaoPedido():
    telaPedidos.close()
    telaPedidos_fazerPedido_validacao.txt_idCliente_fazerPedido.clear()
    telaPedidos_fazerPedido_validacao.txt_idFunc_fazerPedido.clear()
    telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.clear()
    telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.clear()
    telaPedidos_fazerPedido_validacao.show()


def validarPedido():
    global numero_idCliente_pedido, numero_idFunc_pedido
    idCli = telaPedidos_fazerPedido_validacao.txt_idCliente_fazerPedido.text().strip()
    idFunc = telaPedidos_fazerPedido_validacao.txt_idFunc_fazerPedido.text().strip()

    if not idCli or not idFunc:
        if not idCli:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.setText("Preencha o ID do cliente")
        else:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.clear()

        if not idFunc:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.setText("Preencha o ID do funcionário")
        else:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.clear()
        return

    idCli_res = buscarCli_id(idCli)
    idFunc_res = buscarFunc_id(idFunc)

    if idCli_res == 1 and idFunc_res == 1:
        # Salva os IDs validados para usar ao criar o pedido
        numero_idCliente_pedido = int(idCli)
        numero_idFunc_pedido = int(idFunc)

        telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.setText("Cadastrado")
        telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.setText("Cadastrado")
        telaPedidos_fazerPedido_validacao.close()
        telaPedidos_fazerPedido_reservarMesa.show()
        exibirMesasDisponiveis()
    else:
        if idCli_res == 1:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.setText("Cadastrado")
        else:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.setText("Não Cadastrado")

        if idFunc_res == 1:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.setText("Cadastrado")
        else:
            telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.setText("Não Cadastrado")



def buscarCli_id(id):
    try:
        dado = (int(id),)
    except (ValueError, TypeError):
        return 0

    cursor = banco.cursor()
    comando_SQL = "SELECT idCliente FROM cliente WHERE idCliente = %s"
    cursor.execute(comando_SQL, dado)
    resultado = cursor.fetchone()
    return 1 if resultado else 0


def buscarFunc_id(id):
    try:
        dado = (int(id),)
    except (ValueError, TypeError):
        return 0

    cursor = banco.cursor()
    comando_SQL = "SELECT idFunc FROM funcionario WHERE idFunc = %s"
    cursor.execute(comando_SQL, dado)
    resultado = cursor.fetchone()
    return 1 if resultado else 0


def exibirMesasDisponiveis():
    # Verificar no BD as mesas que tem disponivel
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa WHERE status = 'Disponível'"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.setRowCount(len(exibir_mesas))
    telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.setColumnCount(4)

    for i in range(0, len(exibir_mesas)):
         for j in range(0, 4):
            telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.setItem(i, j, QtWidgets.QTableWidgetItem(str(exibir_mesas[i][j])))


def exibir_cardapio_pedido():
    # Popula a tela de exibição de cardápio com os produtos disponíveis
    cursor = banco.cursor()
    cursor.execute("SELECT idProduto, nome, preco, idCategoria FROM produto")
    dados_lidos = cursor.fetchall()

    telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.setRowCount(len(dados_lidos))
    telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.setColumnCount(4)

    for i in range(len(dados_lidos)):
        for j in range(4):
            telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))
            )


def adicionarAoCarrinho():
    """Lê o produto selecionado na tabela, a quantidade e adiciona ao carrinho."""
    global carrinho
    linha = telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.currentRow()

    if linha < 0:
        return

    # Pega dados do produto direto da tabela já carregada
    idProduto  = int(telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.item(linha, 0).text())
    nomeProduto = telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.item(linha, 1).text()
    preco       = float(telaPedidos_fazerPedido_exibirCardapio.tabela_cardapioPedido.item(linha, 2).text())

    try:
        quantidade = int(telaPedidos_fazerPedido_exibirCardapio.txt_quantidade.text().strip())
        if quantidade <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        return

    subTotal = preco * quantidade

    # Se o produto já está no carrinho, soma a quantidade
    for item in carrinho:
        if item['idProduto'] == idProduto:
            item['quantidade'] += quantidade
            item['subTotal']   += subTotal
            atualizarTabelaCarrinho()
            return

    carrinho.append({
        'idProduto':  idProduto,
        'nome':       nomeProduto,
        'preco':      preco,
        'quantidade': quantidade,
        'subTotal':   subTotal
    })
    atualizarTabelaCarrinho()


def atualizarTabelaCarrinho():
    """Reflete o estado atual do carrinho na tabela da tela de cardápio."""
    tabela = telaPedidos_fazerPedido_exibirCardapio.tabela_carrinho
    tabela.setRowCount(len(carrinho))
    tabela.setColumnCount(4)  # nome | preco | quantidade | subTotal

    for i, item in enumerate(carrinho):
        tabela.setItem(i, 0, QtWidgets.QTableWidgetItem(item['nome']))
        tabela.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item['preco'])))
        tabela.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item['quantidade'])))
        tabela.setItem(i, 3, QtWidgets.QTableWidgetItem(str(item['subTotal'])))


def fazerPedido():
    """Confirma o pedido: cria o registro em pedido e insere cada item em itempedido."""
    global carrinho, numero_idCliente_pedido, numero_idFunc_pedido, numero_idMesa

    if not carrinho:
        QtWidgets.QMessageBox.warning(None, "Carrinho vazio", "Adicione pelo menos um produto antes de confirmar o pedido.")
        return

    data = telaPedidos_fazerPedido_exibirCardapio.txt_dataPedido.text().strip()
    if not data:
        QtWidgets.QMessageBox.warning(None, "Data inválida", "Preencha a data do pedido antes de confirmar.")
        return

    total = sum(item['subTotal'] for item in carrinho)
    idProduto_principal = carrinho[0]['idProduto']

    cursor = banco.cursor()
    try:
        # 1. Insere o pedido
        cursor.execute(
            "INSERT INTO pedido (data, total, idCliente, idFunc, idMesa, idProduto) VALUES (%s, %s, %s, %s, %s, %s)",
            (str(data), float(total), int(numero_idCliente_pedido),
             int(numero_idFunc_pedido), int(numero_idMesa), int(idProduto_principal))
        )
        idPedido_novo = cursor.lastrowid

        # 2. Insere cada item no itempedido
        for item in carrinho:
            cursor.execute(
                "INSERT INTO itempedido (subTotal, quantidade, idPedido, idProduto) VALUES (%s, %s, %s, %s)",
                (float(item['subTotal']), int(item['quantidade']),
                 int(idPedido_novo), int(item['idProduto']))
            )

        banco.commit()

    except Exception as e:
        banco.rollback()
        QtWidgets.QMessageBox.critical(None, "Erro", f"Falha ao salvar o pedido:{e}")
        return

    # Limpa o carrinho e volta para a tela de pedidos
    carrinho = []
    telaPedidos_fazerPedido_exibirCardapio.txt_dataPedido.clear()
    telaPedidos_fazerPedido_exibirCardapio.txt_quantidade.clear()
    telaPedidos_fazerPedido_exibirCardapio.tabela_carrinho.setRowCount(0)
    QtWidgets.QMessageBox.information(None, "Sucesso", "Pedido registrado com sucesso!")
    telaPedidos_fazerPedido_exibirCardapio.close()
    atualizarTabelaPedidos()
    telaPedidos.show()


def reservarMesas():
    global numero_idMesa
    linha = telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.currentRow()

    if linha < 0:
        return

    valor_id = int(telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.item(linha, 0).text())

    numero_idMesa = valor_id
    cursor = banco.cursor()
    comando_SQL = "UPDATE mesa SET status = 'Ocupada' WHERE idMesa = %s"
    cursor.execute(comando_SQL, (int(numero_idMesa),))
    banco.commit()

    telaPedidos_fazerPedido_reservarMesa.close()
    exibir_cardapio_pedido()
    telaPedidos_fazerPedido_exibirCardapio.show()
    

def atualizarPedido():
    global numero_idPedido
    linha = telaPedidos.tabela_pedidos.currentRow()

    if linha < 0:
        QtWidgets.QMessageBox.warning(None, "Nenhum pedido selecionado", "Selecione um pedido na tabela antes de atualizar.")
        return

    valor_id = int(telaPedidos.tabela_pedidos.item(linha, 0).text())

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM pedido WHERE idPedido = %s", (valor_id,))
    pedido = cursor.fetchone()

    if not pedido:
        return

    numero_idPedido = valor_id

    telaPedidos_atualizar.txt_dataAtualizarPedido.setText(str(pedido[1]))
    telaPedidos_atualizar.txt_valorAtualizarPedido.setText(str(pedido[2]))
    telaPedidos_atualizar.txt_idCliAtualizarPedido.setText(str(pedido[3]))
    telaPedidos_atualizar.txt_idFuncAtualizarPedido.setText(str(pedido[4]))
    telaPedidos_atualizar.txt_idMesaAtualizarPedido.setText(str(pedido[5]))
    telaPedidos_atualizar.txt_idComidaAtualizarPedido.setText(str(pedido[6]))
    telaPedidos_atualizar.show()


def salvarPedido():
    # pega o numero do id
    global numero_idPedido
    data = telaPedidos_atualizar.txt_dataAtualizarPedido.text()
    valor = telaPedidos_atualizar.txt_valorAtualizarPedido.text()
    idCli = telaPedidos_atualizar.txt_idCliAtualizarPedido.text()
    idFunc = telaPedidos_atualizar.txt_idFuncAtualizarPedido.text()
    idMesa = telaPedidos_atualizar.txt_idMesaAtualizarPedido.text()
    idComida = telaPedidos_atualizar.txt_idComidaAtualizarPedido.text()

    cursor = banco.cursor()
    comando_SQL = "UPDATE pedido SET data = %s, total = %s, idCliente = %s, idFunc = %s, idMesa = %s, idProduto = %s WHERE idPedido = %s"
    dados = (str(data), float(valor), int(idCli), int(idFunc), int(idMesa), int(idComida), int(numero_idPedido))
    cursor.execute(comando_SQL, dados)
    banco.commit()

    # atualizar as janelas
    telaPedidos_atualizar.close()
    telaPedidos.close()
    atualizarTabelaPedidos()


def removerPedido():
    linha = telaPedidos.tabela_pedidos.currentRow()

    if linha < 0:
        QtWidgets.QMessageBox.warning(None, "Nenhum pedido selecionado", "Selecione um pedido antes de remover.")
        return

    valor_id = int(telaPedidos.tabela_pedidos.item(linha, 0).text())

    cursor = banco.cursor()
    # Remove filhos antes de deletar o pedido (respeita FK)
    cursor.execute("DELETE FROM itempedido WHERE idPedido = %s", (valor_id,))
    cursor.execute("DELETE FROM pagamento WHERE idPedido = %s", (valor_id,))
    cursor.execute("DELETE FROM pedido WHERE idPedido = %s", (valor_id,))
    banco.commit()

    atualizarTotalPedidos()
    atualizarTabelaPedidos()


def listarPedidos():
    # Mostrar todos os pedidos cadastrados
    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaPedidos.tabela_pedidos.setRowCount(len(dados_lidos))
    telaPedidos.tabela_pedidos.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
         for j in range(0, 7):
            telaPedidos.tabela_pedidos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    atualizarTotalPedidos()


def atualizarTotalPedidos():
    """Atualiza o contador de total de pedidos exibido na tela."""
    cursor = banco.cursor()
    cursor.execute("SELECT COUNT(*) FROM pedido")
    dado = cursor.fetchone()
    telaPedidos.txt_totalPedidos.setText(f"Total: {dado[0]}")


def atualizarTabelaPedidos():
    telaPedidos.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaPedidos.tabela_pedidos.setRowCount(len(dados_lidos))
    telaPedidos.tabela_pedidos.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
         for j in range(0, 7):
            telaPedidos.tabela_pedidos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    atualizarTotalPedidos()


# Pagamentos  -------------------------------------------------------------------------------------------------------
def gerenciarPagamentos():
    telaPedidos.close()
    exibir_pedidos_pagamento()  # carrega a tabela antes de mostrar a tela
    telaPedidos_pagamento.show()


def exibir_pedidos_pagamento():
    # Popula a tabela da tela de pagamento com todos os pedidos
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM pedido ORDER BY idPedido")
    dados_lidos = cursor.fetchall()

    telaPedidos_pagamento.tabela_pedidosPagamento.setRowCount(len(dados_lidos))
    telaPedidos_pagamento.tabela_pedidosPagamento.setColumnCount(7)

    for i in range(len(dados_lidos)):
        for j in range(7):
            telaPedidos_pagamento.tabela_pedidosPagamento.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))
            )


def confirmarPagamento():
    global numero_idPedido
    linha = telaPedidos_pagamento.tabela_pedidosPagamento.currentRow()

    if linha < 0:
        return

    numero_idPedido = int(telaPedidos_pagamento.tabela_pedidosPagamento.item(linha, 0).text())

    cursor = banco.cursor()
    cursor.execute(
        "SELECT total, idMesa FROM pedido WHERE idPedido = %s",
        (int(numero_idPedido),)
    )
    pedido = cursor.fetchone()

    if not pedido:
        return

    total, idMesa = pedido

    try:
        # 1. Registra o pagamento
        cursor.execute(
            "INSERT INTO pagamento (valor, idPedido) VALUES (%s, %s)",
            (float(total), int(numero_idPedido))
        )

        # 2. Libera a mesa
        cursor.execute(
            "UPDATE mesa SET status = 'Disponível' WHERE idMesa = %s",
            (int(idMesa),)
        )

        # 3. Remove itens do pedido antes de deletar (respeita FK)
        cursor.execute(
            "DELETE FROM itempedido WHERE idPedido = %s",
            (int(numero_idPedido),)
        )

        # 4. Remove o pedido
        cursor.execute(
            "DELETE FROM pedido WHERE idPedido = %s",
            (int(numero_idPedido),)
        )

        banco.commit()
    except Exception as e:
        banco.rollback()
        print(f"Erro ao confirmar pagamento: {e}")
        return

    telaPedidos_pagamento.close()
    telaPedidos.show()
    listarPedidos()


def exibir_cardapio():
    pass  # mantido por compatibilidade; lógica movida para exibir_pedidos_pagamento


# Mesas -------------------------------------------------------------------------------------------------------
def gerenciarMesas():
    telaPrincipal.close()
    telaMesas.show()


def cadastrarMesa():
    telaMesas.close()
    telaMesas_cadastrar.show()


def confirmarCadastro_mesa():
    numero    = telaMesas_cadastrar.txt_numeroCadastrarMesa.text().strip()
    capacidade = telaMesas_cadastrar.txt_qtdCadastrarMesa.text().strip()
    status    = "Disponível"

    if not numero or not capacidade:
        QtWidgets.QMessageBox.warning(None, "Campos obrigatórios", "Preencha o número e a capacidade da mesa.")
        return

    cursor = banco.cursor()

    # Verifica se já existe mesa com esse número
    cursor.execute("SELECT idMesa FROM mesa WHERE numero = %s", (int(numero),))
    if cursor.fetchone():
        QtWidgets.QMessageBox.warning(None, "Mesa já existe", f"Já existe uma mesa com o número {numero}. Escolha outro número.")
        return

    cursor.execute(
        "INSERT INTO mesa (status, numero, capacidade) VALUES (%s, %s, %s)",
        (str(status), int(numero), int(capacidade))
    )
    banco.commit()

    telaMesas_cadastrar.close()
    atualizarTabelaMesas()


def removerMesa():
    linha = telaMesas.tabela_mesas.currentRow()

    if linha == -1:
        QtWidgets.QMessageBox.warning(None, "Nenhuma mesa selecionada", "Selecione uma mesa antes de remover.")
        return

    valor_id = int(telaMesas.tabela_mesas.item(linha, 0).text())

    cursor = banco.cursor()
    cursor.execute("DELETE FROM mesa WHERE idMesa = %s", (valor_id,))
    banco.commit()

    atualizarTabelaMesas()


def listarMesas():
    # Serve para mostrar TODAS as mesas cadastradas no sistema
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    telaMesas.tabela_mesas.setRowCount(len(exibir_mesas))
    telaMesas.tabela_mesas.setColumnCount(4)

    for i in range(0, len(exibir_mesas)):
         for j in range(0, 4):
            telaMesas.tabela_mesas.setItem(i, j, QtWidgets.QTableWidgetItem(str(exibir_mesas[i][j])))


def atualizarTabelaMesas():
    telaMesas.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM mesa"
    cursor.execute(comando_SQL)
    exibir_mesas = cursor.fetchall()

    telaMesas.tabela_mesas.setRowCount(len(exibir_mesas))
    telaMesas.tabela_mesas.setColumnCount(4)

    for i in range(0, len(exibir_mesas)):
         for j in range(0, 4):
            telaMesas.tabela_mesas.setItem(i, j, QtWidgets.QTableWidgetItem(str(exibir_mesas[i][j])))


# COMIDAS  -------------------------------------------------------------------------------------------------------
def gerenciarComidas():
    telaPrincipal.close()
    telaComidas.show()


def cadastrarComida():
    telaComidas.close()
    telaCadastrarProduto.show()


def confirmarCadastro_produto():
    nome      = telaCadastrarProduto.txt_nomeCadastroProduto.text()
    preco     = telaCadastrarProduto.txt_precoCadastroProduto.text()
    categoria = telaCadastrarProduto.txt_categoriaCadastroProduto.text()

    cursor = banco.cursor()
    cursor.execute(
        "INSERT INTO produto (nome, preco, idCategoria) VALUES (%s, %s, %s)",
        (str(nome), float(preco), int(categoria))
    )
    banco.commit()

    telaCadastrarProduto.close()
    atualizarTabelaComidas()


def listarComidas():
    cursor = banco.cursor()
    cursor.execute("SELECT idProduto, nome, preco, idCategoria FROM produto")
    busca = cursor.fetchall()

    telaComidas.tabela_cardapio.setRowCount(len(busca))
    telaComidas.tabela_cardapio.setColumnCount(4)

    for i in range(len(busca)):
        for j in range(4):
            telaComidas.tabela_cardapio.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def removerComida():
    linha = telaComidas.tabela_cardapio.currentRow()

    if linha < 0:
        QtWidgets.QMessageBox.warning(None, "Nenhum produto selecionado", "Selecione um produto antes de remover.")
        return

    valor_id = int(telaComidas.tabela_cardapio.item(linha, 0).text())

    cursor = banco.cursor()
    # Remove itempedido que referenciam esse produto antes de deletar o produto (FK)
    cursor.execute("DELETE FROM itempedido WHERE idProduto = %s", (valor_id,))
    cursor.execute("DELETE FROM produto WHERE idProduto = %s", (valor_id,))
    banco.commit()

    atualizarTabelaComidas()


def atualizarComida():
    global numero_idComida
    linha = telaComidas.tabela_cardapio.currentRow()

    if linha == -1:
        return

    valor_id = telaComidas.tabela_cardapio.item(linha, 0).text()

    cursor = banco.cursor()
    cursor.execute("SELECT idProduto, nome, preco, idCategoria FROM produto WHERE idProduto = %s", (int(valor_id),))
    produto = cursor.fetchone()

    numero_idComida = int(valor_id)

    telaComidas_atualizar.input_nome.setText(str(produto[1]))
    telaComidas_atualizar.input_preco.setText(str(produto[2]))
    telaComidas_atualizar.input_categoria.setText(str(produto[3]))

    telaComidas.close()
    telaComidas_atualizar.show()


def salvarComida():
    global numero_idComida
    nome      = telaComidas_atualizar.input_nome.text()
    preco     = telaComidas_atualizar.input_preco.text()
    categoria = telaComidas_atualizar.input_categoria.text()  # novo

    cursor = banco.cursor()
    cursor.execute(
        "UPDATE produto SET nome = %s, preco = %s, idCategoria = %s WHERE idProduto = %s",
        (str(nome), float(preco), int(categoria), int(numero_idComida))
    )
    banco.commit()

    telaComidas_atualizar.close()
    atualizarTabelaComidas()


def atualizarTabelaComidas():
    telaComidas.show()

    cursor = banco.cursor()
    cursor.execute("SELECT idProduto, nome, preco, idCategoria FROM produto")
    dados_lidos = cursor.fetchall()

    telaComidas.tabela_cardapio.setRowCount(len(dados_lidos))
    telaComidas.tabela_cardapio.setColumnCount(4)

    for i in range(len(dados_lidos)):
        for j in range(4):
            telaComidas.tabela_cardapio.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# faz com que o sistema funcione
app = QtWidgets.QApplication([])

# TODAS as telas que forem criadas tem que fazer isso ai
# Tela principal
ui_path1 = Path(__file__).with_name("telaPrincipal.ui")
telaPrincipal = uic.loadUi(str(ui_path1))

# botões da tela principal
telaPrincipal.bt_gerFunc.clicked.connect(gerenciarFunc)
telaPrincipal.bt_gerFunc.clicked.connect(listarFuncionarios) # esse aqui é pra quando o usuário clicar no botão Gerenciar Funcionário, a tabela carregar
telaPrincipal.bt_gerMesas.clicked.connect(gerenciarMesas)
telaPrincipal.bt_gerMesas.clicked.connect(listarMesas)
telaPrincipal.bt_gerPedidos.clicked.connect(gerenciarPedidos)
telaPrincipal.bt_gerPedidos.clicked.connect(listarPedidos)
telaPrincipal.bt_gerComidas.clicked.connect(gerenciarComidas)
telaPrincipal.bt_gerComidas.clicked.connect(listarComidas)
telaPrincipal.bt_gerCliente.clicked.connect(gerenciarClientes)
telaPrincipal.bt_gerCliente.clicked.connect(listarClientes)

# Tela funcionário
ui_path2 = Path(__file__).with_name("telaFuncionarios.ui")
telaFunc = uic.loadUi(str(ui_path2))

# botoões da tela funcionário
telaFunc.bt_cadastrarFunc.clicked.connect(cadastrarFunc)
telaFunc.bt_buscarFunc.clicked.connect(buscarFunc)
telaFunc.bt_atualizarFunc.clicked.connect(atualizarFunc)
telaFunc.bt_excluirFunc.clicked.connect(removerFuncionario)

# Tela funcionário_cadastro
ui_path3 = Path(__file__).with_name("telaFuncionarios_cadastro.ui")
telaFunc_cadastro = uic.loadUi(str(ui_path3))

# botão da tela funcionário_cadastro
telaFunc_cadastro.bt_confirmarCadastroFun.clicked.connect(confirmarCadastro_func)

# Tela funcionário_atualizar
ui_path4 = Path(__file__).with_name("telaFuncionarios_atualizar.ui")
telaFunc_atualizar = uic.loadUi(str(ui_path4))

# botão da tela funcionário_atualizar
telaFunc_atualizar.bt_confirmarAtualizarFun.clicked.connect(salvarFuncionario)

# Tela mesas 
ui_path10 = Path(__file__).with_name("telaMesas.ui")
telaMesas = uic.loadUi(str(ui_path10))

# botão da tela Mesas
telaMesas.bt_cadastrarMesa.clicked.connect(cadastrarMesa)
telaMesas.bt_removerMesa.clicked.connect(removerMesa)

# Tela mesas_cadastrar
ui_path11 = Path(__file__).with_name("telaMesas_cadastrar.ui")
telaMesas_cadastrar = uic.loadUi(str(ui_path11))

# botão tela mesa_cadastrar
telaMesas_cadastrar.bt_confirmarCadastro_mesa.clicked.connect(confirmarCadastro_mesa)

# tela pedidos
ui_path12 = Path(__file__).with_name("telaPedidos.ui")
telaPedidos = uic.loadUi(str(ui_path12))

# botões da tela mesas
telaPedidos.bt_fazerPedido.clicked.connect(abrirTelaValidacaoPedido)
telaPedidos.bt_removerPedido.clicked.connect(removerPedido)
telaPedidos.bt_atualizarPedido.clicked.connect(atualizarPedido)
telaPedidos.bt_pagamento.clicked.connect(gerenciarPagamentos)

# tela pedidos_atualizar
ui_path13 = Path(__file__).with_name("telaPedidos_atualizar.ui")
telaPedidos_atualizar = uic.loadUi(str(ui_path13))

# botão tela pedido_atualizar
telaPedidos_atualizar.bt_confirmarAtualizarPedido.clicked.connect(salvarPedido)

# tela pedidos_fazerPedido_validacao
ui_path14 = Path(__file__).with_name("telaPedidos_fazerPedido_validacao.ui")
telaPedidos_fazerPedido_validacao = uic.loadUi(str(ui_path14))

# botão da tela pedidos_fazerPedido_validacao
telaPedidos_fazerPedido_validacao.bt_validar.clicked.connect(validarPedido)

# tela pedidos_fazerPedido_reservarMesa
ui_path15 = Path(__file__).with_name("telaPedidos_fazerPedido_reservarMesa.ui")
telaPedidos_fazerPedido_reservarMesa = uic.loadUi(str(ui_path15))

# botão da tela pedidos_fazerPedido_reservarMesa
telaPedidos_fazerPedido_reservarMesa.bt_confirmacaoReservarMesa.clicked.connect(reservarMesas)

# tela pedidos_fazerPedido_exibirCardapio
ui_path16 = Path(__file__).with_name("telaPedidos_fazerPedido_exibirCardapio.ui")
telaPedidos_fazerPedido_exibirCardapio = uic.loadUi(str(ui_path16))

# botões da tela pedidos_fazerPedido_exibirCardapio
telaPedidos_fazerPedido_exibirCardapio.bt_adicionarItem.clicked.connect(adicionarAoCarrinho)
telaPedidos_fazerPedido_exibirCardapio.bt_confirmarPedido.clicked.connect(fazerPedido)

# Tela comidas
ui_path18 = Path(__file__).with_name("telaComidas.ui")
telaComidas = uic.loadUi(str(ui_path18))

telaComidas.bt_atualizarComida.clicked.connect(atualizarComida)
telaComidas.bt_cadastrarComida.clicked.connect(cadastrarComida)
telaComidas.bt_removerComida.clicked.connect(removerComida)

# Tela comidas_atualizar
ui_path19= Path(__file__).with_name("telaAtualizarComida.ui")
telaComidas_atualizar = uic.loadUi(str(ui_path19))

telaComidas_atualizar.bt_salvar.clicked.connect(salvarComida)

# Tela comida_cadastrar
ui_path20 = Path(__file__).with_name("telaCadastrarProduto.ui")
telaCadastrarProduto = uic.loadUi(str(ui_path20))

telaCadastrarProduto.bt_confirmarCadastroProduto.clicked.connect(confirmarCadastro_produto)

# Tela clientes
ui_path21 = Path(__file__).with_name("telaClientes.ui")
telaClientes = uic.loadUi(str(ui_path21))

telaClientes.bt_cadastrarCliente.clicked.connect(cadastrarCliente)
telaClientes.bt_buscarCliente.clicked.connect(buscarCliente)
telaClientes.bt_atualizarCliente.clicked.connect(atualizarCliente)
telaClientes.bt_excluirCliente.clicked.connect(removerCliente)

# Tela clientes_cadastro
ui_path22 = Path(__file__).with_name("telaClientes_cadastro.ui")
telaClientes_cadastro = uic.loadUi(str(ui_path22))

telaClientes_cadastro.bt_confirmarCadastroCliente.clicked.connect(confirmarCadastro_cliente)

# Tela clientes_atualizar
ui_path23 = Path(__file__).with_name("telaClientes_atualizar.ui")
telaClientes_atualizar = uic.loadUi(str(ui_path23))

telaClientes_atualizar.bt_confirmarAtualizarCliente.clicked.connect(salvarCliente)

# Tela pedidos_pagamentos
ui_path24 = Path(__file__).with_name("telaPedidos_pagamento.ui")
telaPedidos_pagamento = uic.loadUi(str(ui_path24))

telaPedidos_pagamento.bt_confirmarPagamento.clicked.connect(confirmarPagamento)


# aqui é pra mostrar a TELA PRINCIPAL DO SISTEMA e executar o SISTEMA

# Conexões dos botões "voltar" de cada tela (centralizadas aqui para não duplicar a cada abertura)
telaClientes.bt_voltar.clicked.connect(lambda: [telaClientes.close(), telaPrincipal.show()])
telaFunc.bt_voltar.clicked.connect(lambda: [telaFunc.close(), telaPrincipal.show()])
telaPedidos.bt_voltar.clicked.connect(lambda: [telaPedidos.close(), telaPrincipal.show()])
telaPedidos_pagamento.bt_voltar.clicked.connect(lambda: [telaPedidos_pagamento.close(), telaPedidos.show()])
telaMesas.bt_voltar.clicked.connect(lambda: [telaMesas.close(), telaPrincipal.show()])
telaComidas.bt_voltar.clicked.connect(lambda: [telaComidas.close(), telaPrincipal.show()])

telaPrincipal.show()
app.exec()