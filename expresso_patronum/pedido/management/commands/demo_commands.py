from django.core.management.base import BaseCommand
from menu.models import Cafe, Ingrediente, BebidaPersonalizada
from pedido.commands import FazerPedidoCommand, CancelarPedidoCommand, AlterarPedidoCommand, InvokerPedidos

class Command(BaseCommand):
    help = 'Demonstra o uso dos Command Patterns no sistema'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧙‍♂️ === DEMONSTRAÇÃO DOS COMMAND PATTERNS === ⚡\n')
        )
        
        # Inicializar dados se necessário
        if not Cafe.objects.exists():
            self.stdout.write('Criando dados iniciais...')
            cafe = Cafe.objects.create(nome="Butterbeer Latte", preco=12.50)
            Ingrediente.objects.create(nome="🥛 Leite de Aveia", preco=1.50)
            Ingrediente.objects.create(nome="🌿 Canela Encantada", preco=1.00)
        
        # Executar demonstração
        self.demonstrar_commands()
    
    def demonstrar_commands(self):
        """Demonstração dos comandos"""
        invoker = InvokerPedidos()
        
        # 1. Fazer pedido
        self.stdout.write('\n1️⃣ FAZENDO PEDIDO:')
        cafe_base = Cafe.objects.first()
        bebida_personalizada = BebidaPersonalizada(cafe_base)
        
        # Adicionar ingredientes
        for ingrediente in Ingrediente.objects.all()[:2]:
            bebida_personalizada.adicionar_ingrediente(ingrediente)
        
        comando_fazer = FazerPedidoCommand(
            cliente="Harry Potter",
            bebida_personalizada=bebida_personalizada,
            observacoes="Extra quente, por favor! ⚡"
        )
        
        resultado = invoker.executar_comando(comando_fazer)
        self.stdout.write(f'   ✅ {resultado["message"]}')
        
        if resultado['success']:
            pedido_id = resultado['pedido'].id
            
            # 2. Alterar pedido
            self.stdout.write('\n2️⃣ ALTERANDO PEDIDO:')
            comando_alterar = AlterarPedidoCommand(
                pedido_id=pedido_id,
                novo_cliente="Harry J. Potter",
                novas_observacoes="Extra quente e bem doce! ⚡✨"
            )
            
            resultado_alterar = invoker.executar_comando(comando_alterar)
            self.stdout.write(f'   ✅ {resultado_alterar["message"]}')
            
            # 3. Desfazer
            self.stdout.write('\n3️⃣ DESFAZENDO ALTERAÇÃO:')
            resultado_desfazer = invoker.desfazer()
            self.stdout.write(f'   ↩️  {resultado_desfazer["message"]}')
            
            # 4. Refazer
            self.stdout.write('\n4️⃣ REFAZENDO ALTERAÇÃO:')
            resultado_refazer = invoker.refazer()
            self.stdout.write(f'   ↪️  {resultado_refazer["message"]}')
            
            # 5. Cancelar
            self.stdout.write('\n5️⃣ CANCELANDO PEDIDO:')
            comando_cancelar = CancelarPedidoCommand(
                pedido_id=pedido_id,
                motivo="Teste de cancelamento"
            )
            
            resultado_cancelar = invoker.executar_comando(comando_cancelar)
            self.stdout.write(f'   ❌ {resultado_cancelar["message"]}')
            
            # 6. Histórico
            self.stdout.write('\n6️⃣ HISTÓRICO DE COMANDOS:')
            historico = invoker.obter_historico()
            for i, item in enumerate(historico):
                status = "✅ Executado" if item['executado'] else "❌ Desfeito"
                self.stdout.write(f'   {i+1}. {item["tipo"]} - {status}')
        
        self.stdout.write(
            self.style.SUCCESS('\n🎯 Demonstração concluída com sucesso!')
        )
