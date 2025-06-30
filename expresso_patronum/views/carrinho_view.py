# View para exibir o carrinho/pedido do cliente
from django.shortcuts import render

def carrinho(request):
    # Exemplo: dados fictícios, depois integrar com sessão/DAO
    pedido = {
        "id": 1,
        "bebida": "Café com leite de aveia, canela, sem açúcar",
        "preco": 7.5,
        "status": "Recebido"
    }
    return render(request, "expresso_patronum/carrinho.html", {"pedido": pedido})
