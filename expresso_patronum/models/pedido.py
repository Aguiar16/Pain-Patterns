# Modelos e padrões relacionados a pedidos
from abc import ABC, abstractmethod
from typing import List
from expresso_patronum.states.estado_pedido import EstadoPedido, RecebidoState

class Observer(ABC):
    @abstractmethod
    def atualizar(self, pedido_id: int, status: str):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def adicionar_observer(self, observer: Observer):
        self._observers.append(observer)

    def remover_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notificar_observers(self, pedido_id: int, status: str):
        for observer in self._observers:
            observer.atualizar(pedido_id, status)

class Pedido(Subject):
    def __init__(self, pedido_id: int, status: str = "Recebido"):
        super().__init__()
        self.pedido_id = pedido_id
        self.status = status
        self.estado: EstadoPedido = RecebidoState()

    def atualizar_status(self, novo_status: str):
        self.status = novo_status
        self.notificar_observers(self.pedido_id, self.status)

    def avancar_estado(self):
        self.estado.proximo_estado(self)
        self.status = self.estado.get_nome()
        self.notificar_observers(self.pedido_id, self.status)
