# Implementação do padrão State para pedidos
from abc import ABC, abstractmethod

class EstadoPedido(ABC):
    @abstractmethod
    def proximo_estado(self, pedido):
        pass
    @abstractmethod
    def get_nome(self) -> str:
        pass

class RecebidoState(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.estado = EmPreparoState()
    def get_nome(self) -> str:
        return "Recebido"

class EmPreparoState(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.estado = ProntoState()
    def get_nome(self) -> str:
        return "Em preparo"

class ProntoState(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.estado = EntregueState()
    def get_nome(self) -> str:
        return "Pronto"

class EntregueState(EstadoPedido):
    def proximo_estado(self, pedido):
        pass  # Estado final
    def get_nome(self) -> str:
        return "Entregue"

class CanceladoState(EstadoPedido):
    def proximo_estado(self, pedido):
        pass  # Estado final
    def get_nome(self) -> str:
        return "Cancelado"

# Exemplo de uso:
# pedido.estado = RecebidoState()
# pedido.estado.proximo_estado(pedido)
# print(pedido.estado.get_nome())
