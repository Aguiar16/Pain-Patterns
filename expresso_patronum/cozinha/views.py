from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from pedido.models import PedidoDAO, Pedido
from .models import CozinhaObserver
from auth_system import admin_required

@admin_required
def painel(request):
    """Painel da cozinha para gerenciar pedidos"""
    # Obter pedidos reais do banco
    todos_pedidos = Pedido.objects.all().order_by('criado_em')
    
    # Estatísticas calculadas
    pedidos_recebidos = todos_pedidos.filter(status='Recebido')
    pedidos_preparo = todos_pedidos.filter(status='Em preparo')
    pedidos_prontos = todos_pedidos.filter(status='Pronto')
    pedidos_entregues_hoje = todos_pedidos.filter(
        status='Entregue',
        criado_em__date=timezone.now().date()
    )
    
    estatisticas = {
        'recebidos': pedidos_recebidos.count(),
        'em_preparo': pedidos_preparo.count(),
        'prontos': pedidos_prontos.count(),
        'entregues_hoje': pedidos_entregues_hoje.count(),
        'tempo_medio': '8:32'  # Poderia ser calculado baseado em dados históricos
    }
    
    # Converter pedidos para formato do template
    def converter_pedido(pedido):
        return {
            'id': str(pedido.id).zfill(3),
            'bebida': pedido.bebida,
            'cliente': pedido.cliente,
            'ingredientes': [],  # Poderia extrair dos detalhes da bebida
            'horario': pedido.criado_em.strftime('%H:%M'),
            'observacoes': '',
            'progresso': 70 if pedido.status == 'Em preparo' else 0,
            'tempo_preparo': '5:30' if pedido.status == 'Em preparo' else '',
            'tempo_pronto': 'Pronto há 2min' if pedido.status == 'Pronto' else ''
        }
    
    # Log de atividades baseado em pedidos recentes
    pedidos_recentes = todos_pedidos.order_by('-criado_em')[:6]
    atividades = []
    
    for pedido in pedidos_recentes:
        tempo = pedido.criado_em.strftime('%H:%M')
        status_map = {
            'Recebido': f'🆕 Novo pedido recebido: #{str(pedido.id).zfill(3)} - {pedido.bebida} ({pedido.cliente})',
            'Em preparo': f'🧙‍♂️ Pedido #{str(pedido.id).zfill(3)} iniciado ({pedido.bebida})',
            'Pronto': f'✅ Pedido #{str(pedido.id).zfill(3)} finalizado e pronto para retirada',
            'Entregue': f'🎉 Pedido #{str(pedido.id).zfill(3)} entregue ao cliente'
        }
        
        atividade_texto = status_map.get(pedido.status, f'Status atualizado: #{str(pedido.id).zfill(3)}')
        atividades.append({
            'time': tempo,
            'text': atividade_texto
        })
    
    context = {
        'estatisticas': estatisticas,
        'pedidos_recebidos': [converter_pedido(p) for p in pedidos_recebidos],
        'pedidos_preparo': [converter_pedido(p) for p in pedidos_preparo],
        'pedidos_prontos': [converter_pedido(p) for p in pedidos_prontos],
        'atividades': atividades,
    }
    
    return render(request, 'cozinha/painel.html', context)

def iniciar_preparo(request, pedido_id):
    """API para iniciar preparo de um pedido"""
    if request.method == 'POST':
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            if pedido.status == 'Recebido':
                pedido.status = 'Em preparo'
                pedido.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Preparo iniciado para pedido #{str(pedido_id).zfill(3)}'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Pedido não pode ser iniciado neste status'
                })
        except Pedido.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Pedido não encontrado'
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
            pedido = Pedido.objects.get(id=pedido_id)
            if pedido.status == 'Em preparo':
                pedido.status = 'Pronto'
                pedido.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Pedido #{str(pedido_id).zfill(3)} está pronto!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Pedido não pode ser marcado como pronto neste status'
                })
        except Pedido.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Pedido não encontrado'
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
            pedido = Pedido.objects.get(id=pedido_id)
            if pedido.status == 'Pronto':
                pedido.status = 'Entregue'
                pedido.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Pedido #{str(pedido_id).zfill(3)} entregue!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Pedido não pode ser marcado como entregue neste status'
                })
        except Pedido.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Pedido não encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def estatisticas(request):
    """API para retornar estatísticas da cozinha"""
    from django.db.models import Count
    from django.utils import timezone
    import datetime
    
    # Pedidos de hoje
    hoje = timezone.now().date()
    pedidos_hoje = Pedido.objects.filter(criado_em__date=hoje)
    
    # Calcular pedidos por hora nas últimas 24h
    pedidos_por_hora = []
    agora = timezone.now()
    for i in range(24):
        hora_inicio = agora - datetime.timedelta(hours=i+1)
        hora_fim = agora - datetime.timedelta(hours=i)
        
        quantidade = Pedido.objects.filter(
            criado_em__gte=hora_inicio,
            criado_em__lt=hora_fim
        ).count()
        
        if quantidade > 0:  # Só adiciona se houver pedidos
            pedidos_por_hora.append({
                'hora': hora_inicio.strftime('%H:00'),
                'quantidade': quantidade
            })
    
    # Top poções mais pedidas
    from django.db.models import Count
    top_pocoes = []
    bebidas_populares = Pedido.objects.values('bebida').annotate(
        quantidade=Count('bebida')
    ).order_by('-quantidade')[:5]
    
    for bebida_data in bebidas_populares:
        top_pocoes.append({
            'nome': bebida_data['bebida'],
            'quantidade': bebida_data['quantidade']
        })
    
    # Tempo médio (placeholder - poderia ser calculado com timestamps reais)
    pedidos_concluidos = Pedido.objects.filter(status='Entregue')
    tempo_medio = '8:32'  # Implementar cálculo real baseado em timestamps
    
    stats = {
        'pedidos_por_hora': pedidos_por_hora[-6:],  # Últimas 6 horas com dados
        'top_pocoes': top_pocoes,
        'tempo_medio_preparo': tempo_medio,
        'pedidos_hoje': pedidos_hoje.count(),
        'total_pedidos': Pedido.objects.count(),
        'pedidos_ativos': Pedido.objects.exclude(status='Entregue').count()
    }
    
    return JsonResponse(stats)
