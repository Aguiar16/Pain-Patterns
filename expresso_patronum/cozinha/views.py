from django.shortcuts import render
from django.http import JsonResponse
from pedido.models import PedidoDAO
from .models import CozinhaObserver

def painel(request):
    """Painel da cozinha para gerenciar pedidos"""
    # Simula dados para o painel da cozinha
    estatisticas = {
        'recebidos': 3,
        'em_preparo': 2,
        'prontos': 1,
        'entregues_hoje': 15,
        'tempo_medio': '8:32'
    }
    
    # Simula pedidos nas diferentes filas
    pedidos_recebidos = [
        {
            'id': '008',
            'bebida': '🍺 Butterbeer Latte',
            'cliente': 'Hermione Granger',
            'ingredientes': ['Leite de Amêndoas', 'Canela Encantada', 'Extra doce'],
            'horario': '16:42',
            'observacoes': 'Bem doce, por favor!'
        },
        {
            'id': '009',
            'bebida': '🦌 Patronus Espresso Duplo',
            'cliente': 'Ron Weasley',
            'ingredientes': ['Açúcar cristal', 'Extra forte'],
            'horario': '16:45',
            'observacoes': ''
        }
    ]
    
    pedidos_preparo = [
        {
            'id': '006',
            'bebida': '🐱 Chá da Prof. McGonagall',
            'cliente': 'Neville Longbottom',
            'ingredientes': ['Mel de abelhas mágicas', 'Limão siciliano'],
            'horario': '16:35',
            'tempo_preparo': '5:30',
            'progresso': 70
        },
        {
            'id': '007',
            'bebida': '🔥 Firewhiskey Coffee',
            'cliente': 'Ginny Weasley',
            'ingredientes': ['Essência de firewhiskey', 'Pimenta encantada', 'Mel dourado'],
            'horario': '16:38',
            'tempo_preparo': '3:15',
            'progresso': 45
        }
    ]
    
    pedidos_prontos = [
        {
            'id': '005',
            'bebida': '🧚 Elixir da Felicidade',
            'cliente': 'Luna Lovegood',
            'ingredientes': ['Xarope de morango', 'Chantilly das nuvens', 'Polvilho dourado'],
            'horario': '16:30',
            'tempo_pronto': 'Pronto há 2min'
        }
    ]
    
    # Log de atividades
    atividades = [
        {'time': '16:45', 'text': '🆕 Novo pedido recebido: #009 - Patronus Espresso (Ron Weasley)'},
        {'time': '16:42', 'text': '🆕 Novo pedido recebido: #008 - Butterbeer Latte (Hermione Granger)'},
        {'time': '16:40', 'text': '🧙‍♂️ Pedido #007 iniciado (Firewhiskey Coffee)'},
        {'time': '16:38', 'text': '✅ Pedido #005 finalizado e pronto para retirada'},
        {'time': '16:35', 'text': '🧙‍♂️ Pedido #006 iniciado (Chá da Prof. McGonagall)'},
        {'time': '16:32', 'text': '🎉 Pedido #004 entregue ao cliente'},
    ]
    
    context = {
        'estatisticas': estatisticas,
        'pedidos_recebidos': pedidos_recebidos,
        'pedidos_preparo': pedidos_preparo,
        'pedidos_prontos': pedidos_prontos,
        'atividades': atividades,
    }
    
    return render(request, 'cozinha/painel.html', context)

def iniciar_preparo(request, pedido_id):
    """API para iniciar preparo de um pedido"""
    if request.method == 'POST':
        try:
            # Aqui seria implementada a lógica para avançar o pedido para "Em Preparo"
            # usando os padrões State e Observer
            
            return JsonResponse({
                'success': True,
                'message': f'Preparo iniciado para pedido #{pedido_id}'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def marcar_pronto(request, pedido_id):
    """API para marcar pedido como pronto"""
    if request.method == 'POST':
        try:
            # Implementaria a lógica para avançar para "Pronto"
            # e notificar observadores
            
            return JsonResponse({
                'success': True,
                'message': f'Pedido #{pedido_id} está pronto!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def marcar_entregue(request, pedido_id):
    """API para marcar pedido como entregue"""
    if request.method == 'POST':
        try:
            # Implementaria a lógica para finalizar o pedido
            
            return JsonResponse({
                'success': True,
                'message': f'Pedido #{pedido_id} entregue!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def estatisticas(request):
    """API para retornar estatísticas da cozinha"""
    stats = {
        'pedidos_por_hora': [
            {'hora': '14:00', 'quantidade': 5},
            {'hora': '15:00', 'quantidade': 8},
            {'hora': '16:00', 'quantidade': 12},
            {'hora': '17:00', 'quantidade': 6},
        ],
        'top_pocoes': [
            {'nome': '🍺 Butterbeer Latte', 'quantidade': 8},
            {'nome': '🦌 Patronus Espresso', 'quantidade': 5},
            {'nome': '🐱 Chá McGonagall', 'quantidade': 3},
        ],
        'tempo_medio_preparo': '8:32',
        'pedidos_hoje': 28
    }
    
    return JsonResponse(stats)
