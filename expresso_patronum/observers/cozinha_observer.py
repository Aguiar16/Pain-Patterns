# Observer para notificação da cozinha
from expresso_patronum.models.pedido import Observer

class CozinhaObserver(Observer):
    def atualizar(self, pedido_id: int, status: str):
        print(f"[COZINHA] Pedido {pedido_id} está agora: {status}")
