from django.db import models

# Strategy: Interface para desconto
class DescontoStrategy:
    def calcular(self, valor):
        raise NotImplementedError

class DescontoFidelidade(DescontoStrategy):
    def calcular(self, valor):
        return valor * 0.90  # 10% de desconto

class DescontoPix(DescontoStrategy):
    def calcular(self, valor):
        return valor * 0.95  # 5% de desconto

class SemDesconto(DescontoStrategy):
    def calcular(self, valor):
        return valor

# Command: Interface para comandos de pagamento
class PagamentoCommand:
    def executar(self, pedido, valor):
        raise NotImplementedError

class PagarPedidoCommand(PagamentoCommand):
    def __init__(self, strategy):
        self.strategy = strategy
    def executar(self, pedido, valor):
        valor_final = self.strategy.calcular(valor)
        # Aqui poderia atualizar status do pedido, registrar pagamento, etc.
        return valor_final

# BO: Lógica de negócio do pagamento
class PagamentoBO:
    @staticmethod
    def sugerir_descontos():
        return [
            ("Cartão Fidelidade", DescontoFidelidade()),
            ("Pix", DescontoPix()),
            ("Cartão Comum", SemDesconto()),
        ]
    @staticmethod
    def processar_pagamento(pedido, tipo_pagamento):
        estrategias = {
            'fidelidade': DescontoFidelidade(),
            'pix': DescontoPix(),
            'cartao': SemDesconto(),
        }
        strategy = estrategias.get(tipo_pagamento, SemDesconto())
        comando = PagarPedidoCommand(strategy)
        return comando.executar(pedido, pedido.preco)
