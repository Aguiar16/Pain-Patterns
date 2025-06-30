# Comando para alterar pedido
from abc import ABC, abstractmethod
from expresso_patronum.models.pedido import Pedido

class AlterarPedidoCommand(Command):
    def __init__(self, pedido: Pedido, novo_status: str):
        self.pedido = pedido
        self.novo_status = novo_status

    def executar(self):
        print(f"Pedido {self.pedido.pedido_id} alterado para {self.novo_status}!")
        self.pedido.atualizar_status(self.novo_status)
