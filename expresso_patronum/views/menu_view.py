# View para exibir o menu de bebidas e personalização
from django.shortcuts import render
from models.bebida import Cafe, Cha

def menu(request):
    bebidas = [
        {"nome": "Café", "preco": Cafe().get_preco()},
        {"nome": "Chá", "preco": Cha().get_preco()},
    ]
    personalizacoes = [
        {"nome": "Leite de Aveia", "preco": 2.0},
        {"nome": "Canela", "preco": 0.5},
        {"nome": "Sem Açúcar", "preco": 0.0},
    ]
    return render(request, "expresso_patronum/menu.html", {"bebidas": bebidas, "personalizacoes": personalizacoes})
