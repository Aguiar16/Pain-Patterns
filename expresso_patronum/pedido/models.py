from django.db import models
# from menu.models import Cafe, Cha, Ingrediente  # Comentado para evitar import circular

# Estados possíveis do pedido (State)
class EstadoPedido:
    def avancar(self, pedido):
        raise NotImplementedError
    def descricao(self):
        raise NotImplementedError

class Recebido(EstadoPedido):
    def avancar(self, pedido):
        pedido.estado = EmPreparo()
    def descricao(self):
        return 'Recebido'

class EmPreparo(EstadoPedido):
    def avancar(self, pedido):
        pedido.estado = Pronto()
    def descricao(self):
        return 'Em preparo'

class Pronto(EstadoPedido):
    def avancar(self, pedido):
        pedido.estado = Entregue()
    def descricao(self):
        return 'Pronto'

class Entregue(EstadoPedido):
    def avancar(self, pedido):
        pass
    def descricao(self):
        return 'Entregue'

# Observer: Interface para notificação
class Observador:
    def notificar(self, pedido):
        raise NotImplementedError

# Pedido model (DAO + BO + Observer + State)
class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    bebida = models.CharField(max_length=100)  # descrição da bebida personalizada
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, default='Recebido')
    observacoes = models.TextField(blank=True, null=True)  # Campo para observações especiais
    criado_em = models.DateTimeField(auto_now_add=True)

    # Estado e observadores não persistidos diretamente
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estado = Recebido()
        self.observadores = []

    def adicionar_observador(self, obs):
        self.observadores.append(obs)

    def avancar_estado(self):
        self.estado.avancar(self)
        self.status = self.estado.descricao()
        self.notificar_observadores()
        self.save()

    def notificar_observadores(self):
        for obs in self.observadores:
            obs.notificar(self)

    def __str__(self):
        return f"Pedido de {self.cliente}: {self.bebida} ({self.status})"

# DAO: Classe de acesso a dados do pedido
class PedidoDAO:
    @staticmethod
    def salvar(pedido):
        pedido.save()
    @staticmethod
    def buscar_por_id(pedido_id):
        return Pedido.objects.get(id=pedido_id)
    @staticmethod
    def listar_todos():
        return Pedido.objects.all()

# BO: Lógica de negócio do pedido
class PedidoBO:
    @staticmethod
    def criar_pedido(cliente, bebida_personalizada):
        pedido = Pedido(
            cliente=cliente,
            bebida=bebida_personalizada.descricao(),
            preco=bebida_personalizada.get_preco(),
        )
        PedidoDAO.salvar(pedido)
        return pedido
    @staticmethod
    def avancar_status(pedido_id):
        pedido = PedidoDAO.buscar_por_id(pedido_id)
        pedido.avancar_estado()
        PedidoDAO.salvar(pedido)
        return pedido
