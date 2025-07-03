from django.db import models

# Observer: Observador da cozinha
class CozinhaObserver:
    def notificar(self, pedido):
        # Aqui pode ser implementada lógica de notificação real (ex: websocket, fila, etc.)
        print(f"[COZINHA] Novo status do pedido: {pedido}")

# Observer: Observador do cliente
class ClienteObserver:
    def __init__(self, cliente_nome):
        self.cliente_nome = cliente_nome
    def notificar(self, pedido):
        print(f"[CLIENTE {self.cliente_nome}] Seu pedido está agora: {pedido.status}")
