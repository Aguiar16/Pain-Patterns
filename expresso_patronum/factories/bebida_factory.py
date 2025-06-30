# Factory Method para bebidas
from expresso_patronum.models.bebida import Bebida, Cafe, Cha
from abc import ABC, abstractmethod

class BebidaFactory(ABC):
    @abstractmethod
    def criar_bebida(self) -> Bebida:
        pass

class CafeFactory(BebidaFactory):
    def criar_bebida(self) -> Bebida:
        return Cafe()

class ChaFactory(BebidaFactory):
    def criar_bebida(self) -> Bebida:
        return Cha()
