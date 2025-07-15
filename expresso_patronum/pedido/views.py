from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Pedido, PedidoBO, PedidoDAO
from cozinha.models import CozinhaObserver, ClienteObserver
from .commands import FazerPedidoCommand, CancelarPedidoCommand, AlterarPedidoCommand, InvokerPedidos

# Instância global do invoker para manter histórico de comandos
invoker_pedidos = InvokerPedidos()

def meus_pedidos(request):
    """Exibe o carrinho do cliente (localStorage) - não mostra histórico de pedidos pagos"""
    # Esta página agora funciona apenas como carrinho
    # O histórico de pedidos pagos será exibido em uma página separada
    context = {
        'carrinho_apenas': True,  # Flag para indicar que é apenas carrinho
    }
    return render(request, 'pedido/meus_pedidos.html', context)

def pagamento(request):
    """Página de finalização do pedido com aplicação de descontos (Strategy)"""
    # Obter itens do carrinho da sessão
    itens_carrinho = request.session.get('carrinho', [])
    
    subtotal = sum(float(item['preco_total']) for item in itens_carrinho)
    
    context = {
        'itens': itens_carrinho,
        'subtotal': subtotal,
    }
    return render(request, 'pedido/pagamento.html', context)

def processar_pagamento(request):
    """Processa o pagamento aplicando a estratégia de desconto escolhida"""
    if request.method == 'POST':
        try:
            tipo_pagamento = request.POST.get('payment_method')
            nome_cliente = request.POST.get('nome', 'Cliente Anônimo')
            
            # Obter itens do carrinho
            itens_carrinho = request.session.get('carrinho', [])
            
            if not itens_carrinho:
                return JsonResponse({
                    'success': False,
                    'message': 'Carrinho vazio!'
                })
            
            # Aplicar padrão Strategy para desconto
            from pagamento.models import PagamentoBO
            
            # Criar pedidos para cada item do carrinho
            pedidos_criados = []
            
            for item in itens_carrinho:
                # Criar objeto de bebida personalizada para aplicar desconto
                class BebidaTemp:
                    def __init__(self, preco):
                        self.preco = preco
                
                bebida_temp = BebidaTemp(item['preco_total'])
                valor_final = PagamentoBO.processar_pagamento(bebida_temp, tipo_pagamento)
                
                # Criar pedido usando BO
                from menu.models import Cafe, BebidaPersonalizada
                cafe_base = Cafe.objects.first()
                if not cafe_base:
                    cafe_base = Cafe.objects.create(nome="Café Base", preco=10.0)
                
                bebida_personalizada = BebidaPersonalizada(cafe_base)
                bebida_personalizada.ingredientes = [{'nome': ing} for ing in item.get('ingredientes', [])]
                
                # Simular descricao e preco
                bebida_personalizada.descricao = lambda: item['descricao_completa']
                bebida_personalizada.get_preco = lambda: valor_final
                
                pedido = PedidoBO.criar_pedido(nome_cliente, bebida_personalizada)
                pedidos_criados.append(pedido)
            
            # Limpar carrinho
            request.session['carrinho'] = []
            request.session.modified = True
            
            # Retornar primeiro pedido como referência
            primeiro_pedido = pedidos_criados[0]
            numero_pedido = f"#{str(primeiro_pedido.id).zfill(3)}"
            
            return JsonResponse({
                'success': True,
                'numero_pedido': numero_pedido,
                'valor_final': sum(float(p.preco) for p in pedidos_criados),
                'message': 'Pagamento processado com sucesso!',
                'pedidos_criados': len(pedidos_criados),
                'redirect_url': '/cliente/historico/'  # Redirecionar para histórico
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao processar pagamento: {str(e)}'
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

# APIs para Command Pattern

def api_fazer_pedido(request):
    """API para fazer pedido usando Command Pattern"""
    if request.method == 'POST':
        try:
            # Obter dados do carrinho
            itens_carrinho = request.session.get('carrinho', [])
            if not itens_carrinho:
                return JsonResponse({
                    'success': False,
                    'message': 'Carrinho vazio'
                })
            
            cliente = request.POST.get('cliente', 'Cliente Anônimo')
            observacoes = request.POST.get('observacoes', '')
            
            resultados = []
            
            # Criar um comando para cada item do carrinho
            for item in itens_carrinho:
                # Criar bebida personalizada do item
                from menu.models import Cafe, BebidaPersonalizada
                cafe_base = Cafe.objects.first()
                if not cafe_base:
                    cafe_base = Cafe.objects.create(nome=item['bebida_nome'], preco=item['bebida_base_preco'])
                
                bebida_personalizada = BebidaPersonalizada(cafe_base)
                
                # Simular adição de ingredientes baseado no item
                for ingrediente_nome in item.get('ingredientes', []):
                    # Aqui seria necessário buscar o ingrediente real ou criar mock
                    pass
                
                # Criar e executar comando
                comando = FazerPedidoCommand(
                    cliente=cliente,
                    bebida_personalizada=bebida_personalizada,
                    observacoes=f"{observacoes} - {item['descricao_completa']}"
                )
                
                resultado = invoker_pedidos.executar_comando(comando)
                resultados.append(resultado)
            
            # Limpar carrinho se todos os pedidos foram bem-sucedidos
            if all(r.get('success', False) for r in resultados):
                request.session['carrinho'] = []
                request.session.modified = True
                
                return JsonResponse({
                    'success': True,
                    'message': f'{len(resultados)} pedido(s) criado(s) com sucesso!',
                    'pedidos': [r.get('pedido').id if r.get('pedido') else None for r in resultados]
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro ao processar alguns pedidos',
                    'detalhes': resultados
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao fazer pedido: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def api_cancelar_pedido(request, pedido_id):
    """API para cancelar pedido usando Command Pattern"""
    if request.method == 'POST':
        try:
            motivo = request.POST.get('motivo', 'Cancelamento solicitado pelo cliente')
            
            # Criar e executar comando de cancelamento
            comando = CancelarPedidoCommand(pedido_id=pedido_id, motivo=motivo)
            resultado = invoker_pedidos.executar_comando(comando)
            
            return JsonResponse(resultado)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao cancelar pedido: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def api_alterar_pedido(request, pedido_id):
    """API para alterar pedido usando Command Pattern"""
    if request.method == 'POST':
        try:
            novo_cliente = request.POST.get('novo_cliente')
            novas_observacoes = request.POST.get('novas_observacoes')
            
            # Para alteração de bebida, seria necessário reconstruir a bebida personalizada
            # Por simplicidade, vamos focar em alterações de cliente e observações
            
            comando = AlterarPedidoCommand(
                pedido_id=pedido_id,
                novo_cliente=novo_cliente,
                novas_observacoes=novas_observacoes
            )
            
            resultado = invoker_pedidos.executar_comando(comando)
            return JsonResponse(resultado)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao alterar pedido: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def api_desfazer_comando(request):
    """API para desfazer último comando"""
    if request.method == 'POST':
        resultado = invoker_pedidos.desfazer()
        return JsonResponse(resultado)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def api_refazer_comando(request):
    """API para refazer comando"""
    if request.method == 'POST':
        resultado = invoker_pedidos.refazer()
        return JsonResponse(resultado)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def api_historico_comandos(request):
    """API para obter histórico de comandos"""
    historico = invoker_pedidos.obter_historico()
    return JsonResponse({
        'success': True,
        'historico': historico
    })

def salvar_pedidos_localstorage(request):
    """API para salvar pedidos do localStorage no banco após pagamento bem-sucedido"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            pedidos_localStorage = data.get('pedidos', [])
            cliente_nome = data.get('cliente', 'Cliente Anônimo')
            
            if not pedidos_localStorage:
                return JsonResponse({
                    'success': False,
                    'message': 'Nenhum pedido para salvar'
                })
            
            pedidos_salvos = []
            
            for item in pedidos_localStorage:
                # Criar pedido no banco
                pedido = Pedido.objects.create(
                    cliente=cliente_nome,
                    bebida=item.get('bebida', 'Bebida Personalizada'),
                    preco=float(item.get('preco', 0)) * int(item.get('quantidade', 1)),
                    observacoes=item.get('observacoes', ''),
                    status='Recebido'
                )
                
                pedidos_salvos.append({
                    'id': pedido.id,
                    'bebida': pedido.bebida,
                    'preco': float(pedido.preco),
                    'status': pedido.status
                })
            
            return JsonResponse({
                'success': True,
                'message': f'{len(pedidos_salvos)} pedido(s) salvo(s) no histórico',
                'pedidos': pedidos_salvos
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar pedidos: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def historico_pedidos(request):
    """Página dedicada ao histórico de pedidos pagos"""
    # Buscar apenas pedidos salvos no banco (após pagamento)
    pedidos_historico = Pedido.objects.all().order_by('-criado_em')
    
    historico_data = []
    for pedido in pedidos_historico:
        # Tenta extrair ingredientes da descrição
        descricao = pedido.bebida
        ingredientes = []
        if 'com ' in descricao:
            partes = descricao.split('com ', 1)
            bebida_base = partes[0].strip()
            ingredientes_str = partes[1].strip()
            ingredientes = [i.strip() for i in ingredientes_str.split(',')]
        else:
            bebida_base = descricao.strip()
        historico_data.append({
            'id': str(pedido.id).zfill(3),
            'bebida': bebida_base,
            'ingredientes': ingredientes,
            'preco': float(pedido.preco),
            'status': pedido.status,
            'horario': pedido.criado_em.strftime('%H:%M'),
            'data': pedido.criado_em.strftime('%d/%m/%Y'),
            'data_completa': pedido.criado_em.strftime('%d/%m/%Y às %H:%M'),
            'observacoes': pedido.observacoes or ''
        })
    
    context = {
        'historico': historico_data,
        'total_pedidos': len(historico_data)
    }
    return render(request, 'pedido/historico_pedidos.html', context)
