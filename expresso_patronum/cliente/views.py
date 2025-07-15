from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auth_system import cliente_required, is_cliente
from pedido.models import Pedido
from .models import ClienteProfile

@cliente_required
def perfil(request):
    """Perfil do cliente com dados de fidelidade"""
    try:
        # Obter ou criar perfil do cliente
        cliente_profile, created = ClienteProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'casa_hogwarts': 'grifinoria',
                'pontos_fidelidade': 0,
                'nivel_fidelidade': 'bronze'
            }
        )
        
        if created:
            messages.info(request, 'Perfil criado com sucesso! Bem-vindo ao Expresso Patronum!')
        
        # Obter pedidos do usuário
        pedidos_recentes = Pedido.objects.filter(
            cliente__icontains=request.user.username
        ).order_by('-criado_em')[:5]
        
        # Calcular estatísticas
        total_pedidos = pedidos_recentes.count()
        valor_economizado = cliente_profile.calcular_desconto(100)  # Exemplo
        progresso = cliente_profile.get_progresso_proximo_nivel()
        
        context = {
            'cliente': cliente_profile,
            'user': request.user,
            'pedidos_recentes': pedidos_recentes,
            'total_pedidos': total_pedidos,
            'valor_economizado': valor_economizado,
            'progresso': progresso,
            'badges': _get_user_badges(cliente_profile),
        }
        
        return render(request, 'cliente/perfil.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao carregar perfil: {str(e)}')
        return render(request, 'cliente/perfil.html', {'error': True})

@cliente_required
def historico(request):
    """Histórico completo de pedidos do cliente"""
    try:
        # Buscar pedidos do usuário (por nome/username)
        pedidos = Pedido.objects.filter(
            cliente__icontains=request.user.username
        ).order_by('-criado_em')
        
        # Estatísticas
        pedidos_concluidos = pedidos.filter(status='Entregue').count()
        pedidos_pendentes = pedidos.exclude(status='Entregue').count()
        valor_total = sum(float(p.preco) for p in pedidos.filter(status='Entregue'))
        
        # Filtros
        filtro_status = request.GET.get('status', '')
        filtro_mes = request.GET.get('mes', '')
        
        if filtro_status:
            pedidos = pedidos.filter(status=filtro_status)
        
        if filtro_mes:
            try:
                ano, mes = filtro_mes.split('-')
                pedidos = pedidos.filter(
                    criado_em__year=int(ano),
                    criado_em__month=int(mes)
                )
            except ValueError:
                pass
        
        context = {
            'pedidos': pedidos,
            'estatisticas': {
                'total': pedidos.count(),
                'concluidos': pedidos_concluidos,
                'pendentes': pedidos_pendentes,
                'valor_total': valor_total,
            },
            'filtro_status': filtro_status,
            'filtro_mes': filtro_mes,
            'status_choices': [
                ('Recebido', 'Recebido'),
                ('Em preparo', 'Em Preparo'),
                ('Pronto', 'Pronto'),
                ('Entregue', 'Entregue'),
            ]
        }
        
        return render(request, 'cliente/historico.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao carregar histórico: {str(e)}')
        return render(request, 'cliente/historico.html', {'error': True})

@cliente_required
def atualizar_perfil(request):
    """API para atualizar dados do perfil do cliente"""
    if request.method == 'POST':
        try:
            cliente_profile = request.user.cliente_profile
            
            # Atualizar dados permitidos
            casa = request.POST.get('casa_hogwarts')
            telefone = request.POST.get('telefone')
            preferencias = request.POST.get('preferencias_bebida')
            
            if casa and casa in dict(ClienteProfile.CASAS_CHOICES):
                cliente_profile.casa_hogwarts = casa
            
            if telefone:
                cliente_profile.telefone = telefone
            
            if preferencias is not None:  # Permite string vazia
                cliente_profile.preferencias_bebida = preferencias
            
            cliente_profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Perfil atualizado com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao atualizar perfil: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def _get_user_badges(cliente_profile):
    """Retorna badges/conquistas do usuário"""
    badges = []
    
    # Badge de fidelidade
    if cliente_profile.nivel_fidelidade == 'ouro':
        badges.append({
            'nome': 'Cliente Ouro',
            'icone': '👑',
            'descricao': 'Nível máximo de fidelidade'
        })
    elif cliente_profile.nivel_fidelidade == 'prata':
        badges.append({
            'nome': 'Cliente Prata',
            'icone': '🥈',
            'descricao': 'Cliente fiel'
        })
    
    # Badge de pedidos
    if cliente_profile.pedidos_realizados >= 50:
        badges.append({
            'nome': 'Viciado em Café',
            'icone': '☕',
            'descricao': '50+ pedidos realizados'
        })
    elif cliente_profile.pedidos_realizados >= 10:
        badges.append({
            'nome': 'Cliente Regular',
            'icone': '🏆',
            'descricao': '10+ pedidos realizados'
        })
    
    # Badge de casa
    casa_badges = {
        'grifinoria': {'nome': 'Corajoso', 'icone': '🦁'},
        'sonserina': {'nome': 'Ambicioso', 'icone': '🐍'},
        'corvinal': {'nome': 'Sábio', 'icone': '🦅'},
        'lufa_lufa': {'nome': 'Leal', 'icone': '🦡'},
    }
    
    if cliente_profile.casa_hogwarts in casa_badges:
        badge = casa_badges[cliente_profile.casa_hogwarts]
        badges.append({
            'nome': f"{badge['nome']} de {cliente_profile.get_casa_hogwarts_display()}",
            'icone': badge['icone'],
            'descricao': f'Membro da casa {cliente_profile.get_casa_hogwarts_display()}'
        })
    
    return badges
