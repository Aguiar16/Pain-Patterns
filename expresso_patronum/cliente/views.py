from django.shortcuts import render
from django.http import JsonResponse

def perfil(request):
    """Perfil do cliente com dados de fidelidade"""
    # Simula dados do cliente
    cliente_data = {
        'nome': 'Harry Potter',
        'email': 'harry@hogwarts.edu',
        'casa': 'Grifinória',
        'fidelidade': True,
        'pontos': 150,
        'pedidos_total': 28,
        'valor_gasto': 'R$ 342,50'
    }
    
    return render(request, 'cliente/perfil.html', {'cliente': cliente_data})

def historico(request):
    """Histórico completo de pedidos do cliente"""
    # Simula histórico de pedidos
    historico = [
        {
            'id': '003',
            'bebida': '🐱 Chá da Prof. McGonagall',
            'data': '01/07/2025',
            'total': 10.80,
            'status': 'Entregue',
            'avaliacao': 5
        },
        {
            'id': '004',
            'bebida': '🔥 Firewhiskey Coffee',
            'data': '30/06/2025',
            'total': 15.50,
            'status': 'Entregue',
            'avaliacao': 4
        },
        # ... mais pedidos
    ]
    
    return render(request, 'cliente/historico.html', {'historico': historico})
