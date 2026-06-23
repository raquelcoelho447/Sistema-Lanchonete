CREATE DATABASE IF NOT EXISTS lanchonete;
USE lanchonete;
 
#tabela cliente
CREATE TABLE IF NOT EXISTS cliente(
    idCliente INT NOT NULL AUTO_INCREMENT,
    telefone VARCHAR(20),
    cpf VARCHAR(20),
    nome VARCHAR(50),
    PRIMARY KEY (idCliente)
);
 
#tabela funcionario (adicionada coluna "funcao", que faltava)
CREATE TABLE IF NOT EXISTS funcionario(
    idFunc INT NOT NULL AUTO_INCREMENT,
    salario DOUBLE,
    cpf VARCHAR(20),
    nome VARCHAR(50),
    funcao VARCHAR(20),
    PRIMARY KEY (idFunc)
);
 
#tabela mesa
CREATE TABLE IF NOT EXISTS mesa(
    idMesa INT NOT NULL AUTO_INCREMENT,
    status VARCHAR(20),
    numero INT,
    capacidade INT,
    tipo VARCHAR(20),
    PRIMARY KEY (idMesa)
);
 
#tabela categoria
CREATE TABLE IF NOT EXISTS categoria(
    idCategoria INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50),
    PRIMARY KEY (idCategoria)
);
 
#tabela produto
CREATE TABLE IF NOT EXISTS produto(
    idProduto INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50),
    preco DOUBLE,
    idCategoria INT,
    PRIMARY KEY (idProduto),
    FOREIGN KEY (idCategoria) REFERENCES categoria(idCategoria)
);
 
#criação da tabela pedido
CREATE TABLE IF NOT EXISTS pedido (
    idPedido INT NOT NULL AUTO_INCREMENT,
    data VARCHAR(20),
    total DOUBLE,
    idCliente INT,
    idFunc INT,
    idMesa INT,
    PRIMARY KEY (idPedido),
    FOREIGN KEY (idCliente) REFERENCES cliente(idCliente),
    FOREIGN KEY (idFunc) REFERENCES funcionario(idFunc),
    FOREIGN KEY (idMesa) REFERENCES mesa(idMesa)
);
 
ALTER TABLE pedido ADD COLUMN idProduto INT;
ALTER TABLE pedido ADD CONSTRAINT fk_pedido_produto FOREIGN KEY (idProduto) REFERENCES produto(idProduto);
 
#tabela itemPedido
CREATE TABLE IF NOT EXISTS itemPedido(
    subTotal DOUBLE,
    quantidade INT,
    idPedido INT,
    idProduto INT,
    PRIMARY KEY (idPedido, idProduto),
    FOREIGN KEY (idPedido) REFERENCES pedido(idPedido),
    FOREIGN KEY (idProduto) REFERENCES produto(idProduto)
);
 
#tabela pagamento (coluna "forma" mantida como no original)
CREATE TABLE IF NOT EXISTS pagamento(
    idPagamento INT NOT NULL AUTO_INCREMENT,
    forma VARCHAR(20) DEFAULT 'Não informado',
    valor DOUBLE,
    idPedido INT,
    PRIMARY KEY(idPagamento),
    FOREIGN KEY (idPedido) REFERENCES pedido(idPedido)
);
 
 
# ===================== INSERINDO DADOS DE TESTE =====================
 
#Categorias
INSERT INTO categoria (nome) VALUES
('Lanches'),
('Bebidas'),
('Sobremesas'),
('Porções'),
('Combos');
 
#Clientes
INSERT INTO cliente (telefone, cpf, nome) VALUES
('(85) 99999-1111', '111.111.111-11', 'Ana Raquel'),
('(85) 99999-2222', '222.222.222-22', 'João Pedro'),
('(85) 99999-3333', '333.333.333-33', 'Maria Clara'),
('(85) 99999-4444', '444.444.444-44', 'Carlos Silva'),
('(85) 99999-5555', '555.555.555-55', 'Fernanda Lima');
 
#Funcionários (coluna corrigida de "tipo" para "funcao")
INSERT INTO funcionario (salario, cpf, nome, funcao) VALUES
(1800.00, '666.666.666-66', 'Lucas Souza', 'Garçom'),
(2200.00, '777.777.777-77', 'Beatriz Santos', 'Caixa'),
(3000.00, '888.888.888-88', 'Rafael Costa', 'Gerente'),
(1800.00, '999.999.999-99', 'Juliana Melo', 'Garçom'),
(2000.00, '000.000.000-00', 'Paulo Henrique', 'Cozinheiro');
 
#Mesas
INSERT INTO mesa (status, numero, capacidade) VALUES
('Disponível', 1, 4),
('Ocupada', 2, 2),
('Disponível', 3, 6),
('Ocupada', 4, 4),
('Disponível', 5, 8);
 
#Produtos
INSERT INTO produto (nome, preco, idCategoria) VALUES
('X-Burguer', 15.00, 1),
('X-Salada', 17.00, 1),
('Coca-Cola', 6.00, 2),
('Suco de Laranja', 8.00, 2),
('Pudim', 10.00, 3),
('Batata Frita', 12.00, 4),
('Combo X-Burguer', 25.00, 5),
('Água Mineral', 4.00, 2);
 
#Pedidos (idProduto adicionado, já que a coluna foi criada pelo ALTER TABLE)
INSERT INTO pedido (data, total, idCliente, idFunc, idMesa, idProduto) VALUES
('2026-06-18', 38.00, 1, 1, 2, 1),
('2026-06-18', 25.00, 2, 4, 4, 7),
('2026-06-17', 47.00, 3, 1, 1, 2),
('2026-06-17', 19.00, 4, 2, 3, 4),
('2026-06-16', 62.00, 5, 3, 5, 7);
 
#ItensPedido
INSERT INTO itemPedido (subTotal, quantidade, idPedido, idProduto) VALUES
(15.00, 1, 1, 1),
(17.00, 1, 1, 2),
(6.00, 1, 1, 3),
(25.00, 1, 2, 7),
(17.00, 1, 3, 2),
(12.00, 2, 3, 6),
(8.00, 1, 3, 4),
(15.00, 1, 4, 1),
(4.00, 1, 4, 8),
(25.00, 2, 5, 7),
(12.00, 1, 5, 6);
 
#Pagamentos (coluna corrigida de "valor, idPedido" sem forma para incluir "forma")
INSERT INTO pagamento (forma, valor, idPedido) VALUES
('Cartão de Crédito', 38.00, 1),
('Pix', 25.00, 2),
('Dinheiro', 47.00, 3),
('Cartão de Débito', 19.00, 4),
('Pix', 62.00, 5);
 
 
# ===================== RELATÓRIOS DE EXEMPLO =====================
 
# Pedidos com total acima de 30
# SELECT idPedido, data, total
# FROM pedido
# WHERE total > 30;
 
# Pedidos com nome do cliente e do atendente
# SELECT
#     pedido.idPedido,
#     cliente.nome AS cliente,
#     funcionario.nome AS atendente,
#     pedido.total
# FROM pedido
# JOIN cliente ON pedido.idCliente = cliente.idCliente
# JOIN funcionario ON pedido.idFunc = funcionario.idFunc;
 