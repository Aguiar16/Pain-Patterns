from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Pedido, PedidoBO, PedidoDAO
from cozinha.models import CozinhaObserver, ClienteObserver

def meus_pedidos(request):
    """Exibe os pedidos do cliente com acompanhamento de status"""
    # Em produção, filtrar por cliente logado
    pedidos = PedidoDAO.listar_todos()
    
    # Simula pedidos para demonstração
    pedidos_demo = [
        {
            'id': '001',
            'bebida': '🍺 Butterbeer Latte Personalizado',
            'personalizacoes': ['Leite de Aveia', 'Canela Encantada', 'Chantilly das Nuvens', 'Sem Açúcar'],
            'preco': 15.50,
            'status': 'Em Preparo',
            'horario': '14:25',
            'progresso': 50
        },
        {
            'id': '002',
            'bebida': '🦌 Patronus Espresso',
            'personalizacoes': ['Açúcar Cristal', 'Duplo'],
            'preco': 9.40,
            'status': 'Pronto',
            'horario': '14:18',
            'progresso': 75
        }
    ]
    
    context = {
        'pedidos_ativos': pedidos_demo,
        'historico': [
            {'id': '003', 'bebida': '🐱 Chá da Prof. McGonagall', 'data': '01/07/2025', 'total': 10.80, 'status': 'Entregue'},
            {'id': '004', 'bebida': '🔥 Firewhiskey Coffee', 'data': '30/06/2025', 'total': 15.50, 'status': 'Entregue'},
            {'id': '005', 'bebida': '🧚 Elixir da Felicidade', 'data': '29/06/2025', 'total': 16.80, 'status': 'Entregue'},
        ]
    }
    return render(request, 'pedido/meus_pedidos.html', context)

def pagamento(request):
    """Página de finalização do pedido com aplicação de descontos (Strategy)"""
    # Simula itens no carrinho
    itens_carrinho = [
        {
            'id': 1,
            'nome': '🍺 Butterbeer Latte Personalizado',
            'personalizacoes': ['Leite de Aveia (+R$ 1,50)', 'Canela Encantada (+R$ 1,00)', 'Chantilly das Nuvens (+R$ 2,50)', 'Sem Açúcar (-R$ 0,50)'],
            'preco': 16.50
        },
        {
            'id': 2,
            'nome': '🦌 Patronus Espresso',
            'personalizacoes': ['Açúcar Cristal (+R$ 0,50)', 'Duplo'],
            'preco': 9.40
        }
    ]
    
    subtotal = sum(item['preco'] for item in itens_carrinho)
    
    context = {
        'itens': itens_carrinho,
        'subtotal': subtotal,
    }
    return render(request, 'pedido/pagamento.html', context)

def processar_pagamento(request):
    """Processa o pagamento aplicando a estratégia de desconto escolhida"""
    if request.method == 'POST':
        tipo_pagamento = request.POST.get('payment_method')
        valor_total = float(request.POST.get('valor_total', 0))
        
        # Aqui seria usada a classe PagamentoBO para aplicar Strategy
        from pagamento.models import PagamentoBO
        valor_final = PagamentoBO.processar_pagamento(None, tipo_pagamento)
        
        # Simula criação do pedido
        numero_pedido = f"#{str(hash(str(valor_final)))[-3:]}"
        
        return JsonResponse({
            'success': True,
            'numero_pedido': numero_pedido,
            'valor_final': valor_final,
            'message': 'Pagamento processado com sucesso!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def avancar_status(request, pedido_id):
    """API para avançar status do pedido (State + Observer)"""
    try:
        pedido = PedidoDAO.buscar_por_id(pedido_id)
        
        # Adiciona observadores
        cozinha_obs = CozinhaObserver()
        cliente_obs = ClienteObserver("Cliente Teste")
        
        pedido.adicionar_observador(cozinha_obs)
        pedido.adicionar_observador(cliente_obs)
        
        # Avança estado usando BO
        pedido_atualizado = PedidoBO.avancar_status(pedido_id)
        
        return JsonResponse({
            'success': True,
            'novo_status': pedido_atualizado.status
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def rastrear_pedido(request, pedido_id):
    """API para rastreamento detalhado do pedido"""
    # Simula dados de rastreamento
    tracking_data = {
        'pedido_id': pedido_id,
        'nome': '🍺 Butterbeer Latte Personalizado',
        'timeline': [
            {'status': 'Pedido Recebido', 'time': '14:25', 'completed': True},
            {'status': 'Em Preparo na Cozinha Mágica', 'time': '14:27', 'completed': True},
            {'status': 'Poção Pronta', 'time': 'Em breve...', 'completed': False},
            {'status': 'Entregue', 'time': 'Aguardando...', 'completed': False},
        ]
    }
    
    return JsonResponse(tracking_data)
