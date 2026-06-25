
#RELATÓRIOS - Sistema de Lanchonete

USE system_lanchonete;

#RELATÓRIO 1 — uso de WHERE
#Lista todos os pedidos com valor total acima de R$ 30,00.

SELECT idPedido, data, total
FROM pedido
WHERE total > 30;


#RELATÓRIO 2 — uso de COUNT + GROUP BY
#quantos pedidos cada cliente já fez.

SELECT cliente.nome, COUNT(pedido.idPedido) AS total_pedidos
FROM cliente
JOIN pedido ON cliente.idCliente = pedido.idCliente
GROUP BY cliente.nome
ORDER BY total_pedidos DESC;


# RELATÓRIO 3 — uso de MAX + JOIN
#Mostra o produto mais caro de cada categoria do cardápio.

SELECT categoria.nome AS categoria, MAX(produto.preco) AS preco_maximo
FROM produto
JOIN categoria ON produto.idCategoria = categoria.idCategoria
GROUP BY categoria.nome
ORDER BY preco_maximo DESC;


# RELATÓRIO EXTRA (opcional) — uso de JOIN com 3 tabelas
# Lista cada pedido com o nome do cliente e do funcionário

SELECT
    pedido.idPedido,
    cliente.nome AS cliente,
    funcionario.nome AS atendente,
    pedido.total
FROM pedido
JOIN cliente ON pedido.idCliente = cliente.idCliente
JOIN funcionario ON pedido.idFunc = funcionario.idFunc
ORDER BY pedido.idPedido;