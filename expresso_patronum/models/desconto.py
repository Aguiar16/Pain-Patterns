# Modelos e padrões relacionados a descontos
from abc import ABC, abstractmethod

class DescontoStrategy(ABC):
    @abstractmethod
    def aplicar_desconto(self, valor: float) -> float:
        pass

class DescontoFidelidade(DescontoStrategy):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.9  # 10% de desconto

class DescontoPix(DescontoStrategy):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.95  # 5% de desconto

class SemDesconto(DescontoStrategy):
    def aplicar_desconto(self, valor: float) -> float:
        return valor  # sem desconto
