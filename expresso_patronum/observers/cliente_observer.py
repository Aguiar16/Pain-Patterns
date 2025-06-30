# Observer para notificação do cliente
from expresso_patronum.models.pedido import Observer

class ClienteObserver(Observer):
    def atualizar(self, pedido_id: int, status: str):
        print(f"[CLIENTE] Seu pedido {pedido_id} está agora: {status}")
