# View para tela de pagamento e descontos
from django.shortcuts import render

def pagamento(request):
    # Exemplo: dados fictícios, depois integrar com lógica de desconto
    valor = 7.5
    descontos = [
        {"nome": "Cartão Fidelidade (10%)", "valor": valor * 0.9},
        {"nome": "Pix (5%)", "valor": valor * 0.95},
        {"nome": "Cartão (sem desconto)", "valor": valor},
    ]
    return render(request, "expresso_patronum/pagamento.html", {"valor": valor, "descontos": descontos})
