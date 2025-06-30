# Modelos e padrões relacionados a bebidas
from abc import ABC, abstractmethod

class Bebida(ABC):
    @abstractmethod
    def get_descricao(self) -> str:
        pass

    @abstractmethod
    def get_preco(self) -> float:
        pass

class Cafe(Bebida):
    def get_descricao(self) -> str:
        return "Café"

    def get_preco(self) -> float:
        return 5.0

class Cha(Bebida):
    def get_descricao(self) -> str:
        return "Chá"

    def get_preco(self) -> float:
        return 4.0

# Decorator para personalização de bebidas
class BebidaDecorator(Bebida):
    def __init__(self, bebida: Bebida):
        self._bebida = bebida

    def get_descricao(self) -> str:
        return self._bebida.get_descricao()

    def get_preco(self) -> float:
        return self._bebida.get_preco()

class LeiteAveia(BebidaDecorator):
    def get_descricao(self) -> str:
        return self._bebida.get_descricao() + ", leite de aveia"

    def get_preco(self) -> float:
        return self._bebida.get_preco() + 2.0

class Canela(BebidaDecorator):
    def get_descricao(self) -> str:
        return self._bebida.get_descricao() + ", canela"

    def get_preco(self) -> float:
        return self._bebida.get_preco() + 0.5

class SemAcucar(BebidaDecorator):
    def get_descricao(self) -> str:
        return self._bebida.get_descricao() + ", sem açúcar"

    def get_preco(self) -> float:
        return self._bebida.get_preco()  # sem custo extra
