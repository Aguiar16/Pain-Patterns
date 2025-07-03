from django.shortcuts import render
from django.http import JsonResponse
from .models import PagamentoBO, DescontoFidelidade, DescontoPix, SemDesconto

def calcular_desconto(request):
    """API para calcular desconto baseado no método de pagamento (Strategy)"""
    if request.method == 'POST':
        tipo_pagamento = request.POST.get('tipo_pagamento')
        valor = float(request.POST.get('valor', 0))
        
        try:
            valor_final = PagamentoBO.processar_pagamento(None, tipo_pagamento)
            desconto = valor - valor_final if valor > valor_final else 0
            
            return JsonResponse({
                'success': True,
                'valor_original': valor,
                'valor_final': valor_final,
                'desconto': desconto,
                'tipo_pagamento': tipo_pagamento
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

def sugerir_descontos(request):
    """API para listar todas as opções de desconto disponíveis"""
    descontos = PagamentoBO.sugerir_descontos()
    
    opcoes = []
    for nome, strategy in descontos:
        # Simula um valor base para mostrar o desconto
        valor_base = 25.90
        valor_com_desconto = strategy.calcular(valor_base)
        
        opcoes.append({
            'nome': nome,
            'desconto_percentual': ((valor_base - valor_com_desconto) / valor_base) * 100 if valor_base > valor_com_desconto else 0,
            'valor_exemplo': valor_com_desconto
        })
    
    return JsonResponse({
        'success': True,
        'opcoes': opcoes
    })
