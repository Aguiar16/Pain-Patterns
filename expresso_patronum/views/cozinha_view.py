# View para tela da cozinha (pedidos em preparo)
from django.shortcuts import render

def cozinha(request):
    # Exemplo: dados fictícios, depois integrar com DAO
    pedidos = [
        {"id": 1, "bebida": "Café com leite de aveia", "status": "Em preparo"},
        {"id": 2, "bebida": "Chá", "status": "Recebido"},
    ]
    return render(request, "expresso_patronum/cozinha.html", {"pedidos": pedidos})
