# Comando para fazer pedido
from abc import ABC, abstractmethod
from expresso_patronum.models.pedido import Pedido

class Command(ABC):
    @abstractmethod
    def executar(self):
        pass

class FazerPedidoCommand(Command):
    def __init__(self, pedido: Pedido):
        self.pedido = pedido

    def executar(self):
        print(f"Pedido {self.pedido.pedido_id} realizado!")
        self.pedido.atualizar_status("Em preparo")
