# Exemplo de fluxo integrando todos os padrões do sistema Expresso Patronum
from models.bebida import Cafe, LeiteAveia, Canela, SemAcucar
from expresso_patronum.factories.bebida_factory import CafeFactory
from models.pedido import Pedido
from models.desconto import DescontoFidelidade, DescontoPix, SemDesconto
from expresso_patronum.observers.cliente_observer import ClienteObserver
from expresso_patronum.observers.cozinha_observer import CozinhaObserver
from models.dao import PedidoDAO
from expresso_patronum.bo.pedido_bo import PedidoBO
from expresso_patronum.commands.fazer_pedido import FazerPedidoCommand
from expresso_patronum.commands.cancelar_pedido import CancelarPedidoCommand
from expresso_patronum.commands.alterar_pedido import AlterarPedidoCommand

# 1. Cliente escolhe bebida base e personalizações
bebida = CafeFactory().criar_bebida()
bebida = LeiteAveia(bebida)
bebida = Canela(bebida)
bebida = SemAcucar(bebida)
print(f"Bebida escolhida: {bebida.get_descricao()} | Preço: R${bebida.get_preco():.2f}")

# 2. Criação do pedido
pedido = Pedido(pedido_id=1)

# 3. Observers (cozinha e cliente)
pedido.adicionar_observer(ClienteObserver())
pedido.adicionar_observer(CozinhaObserver())

# 4. DAO e BO
dao = PedidoDAO()
bo = PedidoBO(dao)
bo.criar_pedido(pedido)

# 5. Comando para fazer pedido
cmd_fazer = FazerPedidoCommand(pedido)
cmd_fazer.executar()

# 6. Avançar estado do pedido (em preparo -> pronto -> entregue)
pedido.avancar_estado()  # Pronto
pedido.avancar_estado()  # Entregue

# 7. Aplicar desconto
valor = bebida.get_preco()
desconto = DescontoFidelidade()  # ou DescontoPix(), SemDesconto()
valor_final = desconto.aplicar_desconto(valor)
print(f"Valor final com desconto: R${valor_final:.2f}")

# 8. Cancelar pedido (opcional)
# cmd_cancelar = CancelarPedidoCommand(pedido)
# cmd_cancelar.executar()
