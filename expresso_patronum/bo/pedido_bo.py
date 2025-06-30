# Lógica de negócio para pedidos
from expresso_patronum.models.pedido import Pedido
from expresso_patronum.models.dao import PedidoDAO

class PedidoBO:
    def __init__(self, dao: PedidoDAO):
        self.dao = dao

    def criar_pedido(self, pedido: Pedido):
        # Lógica de negócio extra pode ser adicionada aqui
        self.dao.salvar(pedido)

    def atualizar_status(self, pedido_id: int, novo_status: str):
        pedido = self.dao.buscar(pedido_id)
        if pedido:
            pedido.atualizar_status(novo_status)
            self.dao.salvar(pedido)

    def listar_pedidos(self):
        return self.dao.listar()
