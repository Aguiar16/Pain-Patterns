# Exemplo de uso completo dos Command Patterns no sistema Expresso Patronum
from menu.models import Cafe, BebidaPersonalizada, Ingrediente
from pedido.commands import FazerPedidoCommand, CancelarPedidoCommand, AlterarPedidoCommand, InvokerPedidos
from pedido.models import Pedido

def demonstrar_commands():
    """Demonstração completa do uso dos Command Patterns"""
    
    print("🧙‍♂️ === DEMONSTRAÇÃO DOS COMMAND PATTERNS === ⚡\n")
    
    # Inicializar invoker
    invoker = InvokerPedidos()
    
    # === 1. FAZER PEDIDO ===
    print("1️⃣ FAZENDO PEDIDO usando FazerPedidoCommand:")
    
    # Criar bebida base
    cafe_base = Cafe.objects.first()
    if not cafe_base:
        cafe_base = Cafe.objects.create(nome="Butterbeer Latte", preco=12.50)
    
    # Criar bebida personalizada (Decorator Pattern)
    bebida_personalizada = BebidaPersonalizada(cafe_base)
    
    # Adicionar ingredientes se existirem
    try:
        leite_aveia = Ingrediente.objects.filter(nome__contains="Aveia").first()
        canela = Ingrediente.objects.filter(nome__contains="Canela").first()
        
        if leite_aveia:
            bebida_personalizada.adicionar_ingrediente(leite_aveia)
        if canela:
            bebida_personalizada.adicionar_ingrediente(canela)
    except:
        print("   ℹ️  Ingredientes não encontrados, usando bebida base")
    
    # Criar e executar comando
    comando_fazer = FazerPedidoCommand(
        cliente="Harry Potter",
        bebida_personalizada=bebida_personalizada,
        observacoes="Extra quente, por favor! ⚡"
    )
    
    resultado = invoker.executar_comando(comando_fazer)
    print(f"   Resultado: {resultado['message']}")
    
    if resultado['success']:
        pedido_id = resultado['pedido'].id
        print(f"   📋 Pedido #{pedido_id} criado com sucesso!\n")
        
        # === 2. ALTERAR PEDIDO ===
        print("2️⃣ ALTERANDO PEDIDO usando AlterarPedidoCommand:")
        
        comando_alterar = AlterarPedidoCommand(
            pedido_id=pedido_id,
            novo_cliente="Harry J. Potter",
            novas_observacoes="Extra quente e bem doce, por favor! ⚡✨"
        )
        
        resultado_alterar = invoker.executar_comando(comando_alterar)
        print(f"   Resultado: {resultado_alterar['message']}\n")
        
        # === 3. DEMONSTRAR DESFAZER ===
        print("3️⃣ DESFAZENDO ÚLTIMA ALTERAÇÃO:")
        
        resultado_desfazer = invoker.desfazer()
        print(f"   Resultado: {resultado_desfazer['message']}\n")
        
        # === 4. REFAZER ===
        print("4️⃣ REFAZENDO ALTERAÇÃO:")
        
        resultado_refazer = invoker.refazer()
        print(f"   Resultado: {resultado_refazer['message']}\n")
        
        # === 5. CANCELAR PEDIDO ===
        print("5️⃣ CANCELANDO PEDIDO usando CancelarPedidoCommand:")
        
        comando_cancelar = CancelarPedidoCommand(
            pedido_id=pedido_id,
            motivo="Cliente desistiu da compra"
        )
        
        resultado_cancelar = invoker.executar_comando(comando_cancelar)
        print(f"   Resultado: {resultado_cancelar['message']}\n")
        
        # === 6. HISTÓRICO DE COMANDOS ===
        print("6️⃣ HISTÓRICO DE COMANDOS EXECUTADOS:")
        
        historico = invoker.obter_historico()
        for i, item in enumerate(historico):
            status = "✅ Executado" if item['executado'] else "❌ Desfeito"
            print(f"   {i+1}. {item['tipo']} - {status}")
        
        print(f"\n📊 Total de comandos no histórico: {len(historico)}")
        
        # === 7. DEMONSTRAR MÚLTIPLOS DESFAZER ===
        print("\n7️⃣ DESFAZENDO MÚLTIPLOS COMANDOS:")
        
        while invoker.indice_atual >= 0:
            resultado = invoker.desfazer()
            if resultado['success']:
                print(f"   ↩️  {resultado['message']}")
            else:
                break
        
        print(f"\n🎯 Demonstração concluída com sucesso!")
        
    else:
        print(f"❌ Erro ao criar pedido: {resultado['message']}")

def demonstrar_cenario_restaurante():
    """Cenário realista de uso dos comandos em um restaurante"""
    
    print("\n🏪 === CENÁRIO REALISTA: DIA NA CAFETERIA === ☕\n")
    
    invoker = InvokerPedidos()
    
    # Cenário 1: Cliente faz pedido
    print("📱 Cliente Harry faz pedido pelo app...")
    cafe_base = Cafe.objects.first() or Cafe.objects.create(nome="Patronus Espresso", preco=8.90)
    bebida = BebidaPersonalizada(cafe_base)
    
    cmd1 = FazerPedidoCommand("Harry Potter", bebida, "Sem açúcar")
    resultado1 = invoker.executar_comando(cmd1)
    pedido_harry = resultado1['pedido'].id if resultado1['success'] else None
    print(f"   {resultado1['message']}")
    
    # Cenário 2: Cliente muda de ideia
    print("\n💭 Harry muda de ideia e quer alterar o pedido...")
    cmd2 = AlterarPedidoCommand(pedido_harry, novas_observacoes="Com açúcar, por favor!")
    resultado2 = invoker.executar_comando(cmd2)
    print(f"   {resultado2['message']}")
    
    # Cenário 3: Problema na cozinha - cancelamento
    print("\n🔥 Problema na máquina de café - pedido cancelado...")
    cmd3 = CancelarPedidoCommand(pedido_harry, "Equipamento com defeito")
    resultado3 = invoker.executar_comando(cmd3)
    print(f"   {resultado3['message']}")
    
    # Cenário 4: Máquina volta a funcionar - desfazer cancelamento
    print("\n🔧 Máquina consertada! Desfazendo cancelamento...")
    resultado4 = invoker.desfazer()
    print(f"   {resultado4['message']}")
    
    # Cenário 5: Novo cliente
    print("\n👤 Nova cliente Hermione faz pedido...")
    cmd5 = FazerPedidoCommand("Hermione Granger", bebida, "Bem forte!")
    resultado5 = invoker.executar_comando(cmd5)
    print(f"   {resultado5['message']}")
    
    print(f"\n📈 Total de operações realizadas: {len(invoker.historico_comandos)}")
    print("✨ Sistema funcionando perfeitamente com Command Pattern!")

if __name__ == "__main__":
    # Executar demonstrações
    demonstrar_commands()
    demonstrar_cenario_restaurante()
