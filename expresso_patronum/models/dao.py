# Implementação do padrão DAO
from expresso_patronum.models.pedido import Pedido

class PedidoDAO:
    def __init__(self):
        self._db = {}  # Simulação de banco de dados em memória

    def salvar(self, pedido: Pedido):
        self._db[pedido.pedido_id] = pedido

    def buscar(self, pedido_id: int) -> Pedido:
        return self._db.get(pedido_id)

    def listar(self):
        return list(self._db.values())

    def remover(self, pedido_id: int):
        if pedido_id in self._db:
            del self._db[pedido_id]
