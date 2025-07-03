from django.shortcuts import render
from django.http import JsonResponse
from .models import Cafe, Cha, Ingrediente, BebidaPersonalizada
# from .factories import BebidaFactory  # Importar quando necessário

def home(request):
    """Página inicial do Expresso Patronum"""
    return render(request, 'menu/home.html')

def cardapio(request):
    """Exibe o cardápio completo com todas as bebidas"""
    cafes = Cafe.objects.all()
    chas = Cha.objects.all()
    ingredientes = Ingrediente.objects.all()
    
    context = {
        'cafes': cafes,
        'chas': chas,
        'ingredientes': ingredientes,
    }
    return render(request, 'menu/cardapio.html', context)

def personalizar(request, bebida_slug):
    """Página de personalização de bebidas usando padrão Decorator"""
    # Simula dados das bebidas (em produção viria do banco)
    bebidas_info = {
        'butterbeer': {
            'nome': '🍺 Butterbeer Latte',
            'descricao': 'Café cremoso inspirado na famosa bebida de Hogwarts, com notas de caramelo, especiarias e uma pitada de magia dourada.',
            'preco': 12.50
        },
        'patronus': {
            'nome': '🦌 Patronus Espresso',
            'descricao': 'Um espresso puro e poderoso que desperta sua energia interior, forte o suficiente para conjurar um Patronus.',
            'preco': 8.90
        },
        'mcgonagall': {
            'nome': '🐱 Chá da Prof. McGonagall',
            'descricao': 'Um chá refinado e elegante, com blend de ervas especiais que acalma até mesmo o coração mais agitado.',
            'preco': 9.80
        },
        'snape': {
            'nome': '🐍 Poção do Professor Snape',
            'descricao': 'Um chá misterioso e complexo, com sabores profundos que revelam suas nuances lentamente.',
            'preco': 13.90
        },
        'firewhiskey': {
            'nome': '🔥 Firewhiskey Coffee',
            'descricao': 'Uma bebida corajosa para momentos especiais, com um toque picante que aquece o coração.',
            'preco': 15.50
        },
        'felicidade': {
            'nome': '🧚 Elixir da Felicidade',
            'descricao': 'Uma bebida doce e reconfortante que traz alegria instantânea.',
            'preco': 14.80
        }
    }
    
    bebida_info = bebidas_info.get(bebida_slug, bebidas_info['butterbeer'])
    ingredientes = Ingrediente.objects.all() if Ingrediente.objects.exists() else []
    
    context = {
        'bebida': bebida_info,
        'ingredientes': ingredientes,
        'bebida_slug': bebida_slug,
    }
    return render(request, 'menu/personalizar.html', context)

def adicionar_ao_carrinho(request):
    """API para adicionar bebida personalizada ao carrinho usando padrão Decorator"""
    if request.method == 'POST':
        # Aqui seria implementada a lógica do padrão Decorator
        # para compor a bebida com os ingredientes selecionados
        
        return JsonResponse({
            'success': True,
            'message': 'Poção adicionada ao caldeirão com sucesso!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})
