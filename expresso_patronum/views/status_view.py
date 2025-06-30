# View para acompanhamento do status do pedido
from django.shortcuts import render

def status_pedido(request):
    # Exemplo: dados fictícios, depois integrar com DAO
    pedido = {
        "id": 1,
        "status": "Pronto",
        "historico": ["Recebido", "Em preparo", "Pronto"]
    }
    return render(request, "expresso_patronum/status.html", {"pedido": pedido})
