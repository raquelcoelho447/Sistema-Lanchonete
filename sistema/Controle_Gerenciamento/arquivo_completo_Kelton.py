from pathlib import Path
import mysql.connector
from PyQt5 import uic, QtWidgets

numero_idFunc = 0
numero_idPedido = 0
numero_idMesa = 0
idCli_res = 0
idFunc_res = 0
numero_idComid = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Vieira_maria22",
    database="lanchonete"
)

# Funcionários -------------------------------------------------------------------------------------------------------
def gerenciarFunc():
    telaPrincipal.close()
    telaFunc.show()

    telaFunc.bt_voltar.clicked.connect(lambda: [telaFunc.close(), telaPrincipal.show()])


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
    telaFunc.show()


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
        return

    valor_id = telaFunc.tabela_funcionarios.item(linha, 0).text()

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM funcionario WHERE idFunc = %s", (int(valor_id),))
    func = cursor.fetchone()

    numero_idFunc = int(valor_id)

    telaFunc_atualizar.txt_nomeAtualizarFunc.setText(str(func[3]))
    telaFunc_atualizar.txt_salarioAtualizarFunc.setText(str(func[1]))
    telaFunc_atualizar.txt_funcaoAtualizarFunc.setText(str(func[4]))
    telaFunc_atualizar.show()


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
        return

    valor_id = telaFunc.tabela_funcionarios.item(linha, 0).text()
    telaFunc.tabela_funcionarios.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("DELETE FROM funcionario WHERE idFunc = %s", (int(valor_id),))
    banco.commit()


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

    telaPedidos.bt_voltar.clicked.connect(lambda: [telaPedidos.close(), telaPrincipal.show()])


def abrirTelaValidacaoPedido():
    telaPedidos.close()
    telaPedidos_fazerPedido_validacao.txt_idCliente_fazerPedido.clear()
    telaPedidos_fazerPedido_validacao.txt_idFunc_fazerPedido.clear()
    telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_cli.clear()
    telaPedidos_fazerPedido_validacao.txt_resultadoValidacao_func.clear()
    telaPedidos_fazerPedido_validacao.show()


def validarPedido():
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


def reservarMesas():
    global numero_idMesa
    linha = telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.currentRow()

    if linha == -1:
        return

    valor_id = telaPedidos_fazerPedido_reservarMesa.tabela_mesasPedidos.item(linha, 0).text()

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM mesa WHERE idMesa = %s", (int(valor_id),))
    pedido = cursor.fetchone()

    if pedido:
        numero_idMesa = int(valor_id)
        cursor.execute("UPDATE mesa SET status = 'Ocupada' WHERE idMesa = %s", (numero_idMesa,))
        banco.commit()
        telaPedidos_fazerPedido_reservarMesa.close()
        telaPedidos_fazerPedido_exibirCardapio.show()
    else:
        telaPedidos_fazerPedido_reservarMesa.close()
        telaPedidos.show()
    

def atualizarPedido():
    global numero_idPedido
    linha = telaPedidos.tabela_pedidos.currentRow()

    if linha == -1:
        return

    valor_id = telaPedidos.tabela_pedidos.item(linha, 0).text()

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM pedido WHERE idPedido = %s", (int(valor_id),))
    pedido = cursor.fetchone()

    numero_idPedido = int(valor_id)

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

    if linha == -1:
        return

    valor_id = telaPedidos.tabela_pedidos.item(linha, 0).text()
    telaPedidos.tabela_pedidos.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("DELETE FROM pedido WHERE idPedido = %s", (int(valor_id),))
    banco.commit()


def listarPedidos():
    # Mostrar todos os pedidos cadastrados
    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaPedidos.tabela_pedidos.setRowCount(len(dados_lidos))
    telaPedidos.tabela_pedidos.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
         for j in range(0, 6):
            telaPedidos.tabela_pedidos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def atualizarTabelaPedidos():
    telaPedidos.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * from pedido"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaPedidos.tabela_pedidos.setRowCount(len(dados_lidos))
    telaPedidos.tabela_pedidos.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
         for j in range(0, 6):
            telaPedidos.tabela_pedidos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# Mesas -------------------------------------------------------------------------------------------------------
def gerenciarMesas():
    telaPrincipal.close()
    telaMesas.show()

    telaMesas.bt_voltar.clicked.connect(lambda: [telaMesas.close(), telaPrincipal.show()])


def cadastrarMesa():
    telaMesas.close()
    telaMesas_cadastrar.show()


def confirmarCadastro_mesa():
    numero = telaMesas_cadastrar.txt_numeroCadastrarMesa.text()
    # se JÁ EXISTER O NUMERO, NÃO CADASTRAR
    capacidade  = telaMesas_cadastrar.txt_qtdCadastrarMesa.text()
    status = "Disponível"

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO mesa (status, numero, capacidade) VALUES (%s, %s, %s)"
    dados_lidos = (str(status), int(numero), int(capacidade))
    cursor.execute(comando_SQL, dados_lidos)
    banco.commit()

    telaMesas_cadastrar.close()
    atualizarTabelaMesas()
    telaMesas.show()


def removerMesa():
    linha = telaMesas.tabela_mesas.currentRow()

    if linha == -1:
        return

    valor_id = telaMesas.tabela_mesas.item(linha, 0).text()
    telaMesas.tabela_mesas.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("DELETE from mesa WHERE idMesa = %s", (int(valor_id),))
    banco.commit()


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
    telaComidas.bt_voltar.clicked.connect(lambda: [telaComidas.close(), telaPrincipal.show()])


def cadastrarComida():
    telaComidas.close()
    telaCadastrarProduto.show()




def listarComidas():
    cursor = banco.cursor()
    cursor.execute("SELECT idProduto, nome, preco, idCategoria FROM produto")
    busca = cursor.fetchall()

    telaComidas.tabela_cardapio.setRowCount(len(busca))
    telaComidas.tabela_cardapio.setColumnCount(4)

    for i in range(len(busca)):
        for j in range(4):
            telaComidas.tabela_cardapio.setItem(i, j, QtWidgets.QTableWidgetItem(str(busca[i][j])))


def atualizarComida():
    global numero_idComid
    linha = telaComidas.tabela_cardapio.currentRow()

    if linha == -1:
        return

    valor_id = telaComidas.tabela_cardapio.item(linha, 0).text()

    cursor = banco.cursor()
    cursor.execute("SELECT idProduto, nome, preco, idCategoria FROM produto WHERE idProduto = %s", (int(valor_id),))
    produto = cursor.fetchone()

    numero_idComid = int(valor_id)

    telaComidas_atualizar.input_nome.setText(str(produto[1]))
    telaComidas_atualizar.input_preco.setText(str(produto[2]))
    telaComidas_atualizar.input_categoria.setText(str(produto[3]))

    telaComidas.close()
    telaComidas_atualizar.show()

def salvarComida():
    global numero_idComid
    nome      = telaComidas_atualizar.input_nome.text()
    preco     = telaComidas_atualizar.input_preco.text()
    categoria = telaComidas_atualizar.input_categoria.text()

    cursor = banco.cursor()
    cursor.execute(
        "UPDATE produto SET nome = %s, preco = %s, idCategoria = %s WHERE idProduto = %s",
        (str(nome), float(preco), int(categoria), int(numero_idComid))
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
# telaPedidos.bt_pagamento.clicked.connect()

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

# botão da tela pedidos_fazerPedido_exibirCardapio


# telaPedidos_fazerPedido_exibirCardapio

# Tela comidas
ui_path18 = Path(__file__).with_name("telaComidas.ui")
telaComidas = uic.loadUi(str(ui_path18))

telaComidas.bt_atualizarComida.clicked.connect(atualizarComida)

# Tela comidas_atualizar
ui_path19= Path(__file__).with_name("telaAtualizarComida.ui")
telaComidas_atualizar = uic.loadUi(str(ui_path19))

telaComidas_atualizar.bt_salvar.clicked.connect(salvarComida)

# Tela comida_cadastrar
ui_path20 = Path(__file__).with_name("telaCadastrarProduto.ui")
telaCadastrarProduto = uic.loadUi(str(ui_path20))

# aqui é pra mostrar a TELA PRINCIPAL DO SISTEMA e executar o SISTEMA
telaPrincipal.show()
app.exec()


