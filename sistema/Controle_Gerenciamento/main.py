from pathlib import Path
from PyQt5 import uic, QtWidgets

PASTA = Path(__file__).parent

# Lista para manter referência das janelas abertas
# (sem isso, o Python "esquece" a janela e ela fecha sozinha)
janelas_abertas = []


def abrir_tela(nome_arquivo_ui):
    caminho = PASTA / nome_arquivo_ui
    tela = uic.loadUi(str(caminho))
    janelas_abertas.append(tela)
    tela.show()
    return tela


def abrir_tela_clientes():
    abrir_tela("telaPrincipal.ui")  # placeholder até existir telaClientes.ui


def abrir_tela_funcionarios():
    abrir_tela("telaFuncionários.ui")


def abrir_tela_pedidos():
    abrir_tela("telaPedidos.ui")


def abrir_tela_mesas():
    abrir_tela("telaMesas.ui")


def abrir_tela_comidas():
    abrir_tela("telaComidas.ui")


def main():
    app = QtWidgets.QApplication([])

    telaPrincipal = uic.loadUi(str(PASTA / "telaPrincipal.ui"))

    telaPrincipal.bt_gerCliente.clicked.connect(abrir_tela_clientes)
    telaPrincipal.bt_gerFunc.clicked.connect(abrir_tela_funcionarios)
    telaPrincipal.bt_gerPedidos.clicked.connect(abrir_tela_pedidos)
    telaPrincipal.bt_gerMesas.clicked.connect(abrir_tela_mesas)
    telaPrincipal.bt_gerComidas.clicked.connect(abrir_tela_comidas)

    telaPrincipal.show()
    app.exec()


if __name__ == "__main__":
    main()