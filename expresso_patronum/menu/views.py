from django.shortcuts import render
from django.http import JsonResponse
from .models import Cafe, Cha, Ingrediente, BebidaPersonalizada
# from .factories import BebidaFactory  # Importar quando necessário

def _criar_dados_iniciais():
    """Cria dados iniciais no banco se não existirem"""
    # Criar Cafés
    if not Cafe.objects.exists():
        cafes_data = [
            {'nome': '🍺 Butterbeer Latte', 'preco': 12.50},
            {'nome': '🦌 Patronus Espresso', 'preco': 8.90},
            {'nome': '📚 Café da Biblioteca', 'preco': 11.20},
            {'nome': '🔥 Firewhiskey Coffee', 'preco': 15.50},
        ]
        for cafe_data in cafes_data:
            Cafe.objects.create(**cafe_data)
    
    # Criar Chás
    if not Cha.objects.exists():
        chas_data = [
            {'nome': '🐱 Chá da Prof. McGonagall', 'preco': 9.80},
            {'nome': '🐍 Poção do Professor Snape', 'preco': 13.90},
        ]
        for cha_data in chas_data:
            Cha.objects.create(**cha_data)
    
    # Criar Ingredientes
    if not Ingrediente.objects.exists():
        ingredientes_data = [
            # Leites
            {'nome': '🥛 Leite de Aveia', 'preco': 1.50},
            {'nome': '🌰 Leite de Amêndoas', 'preco': 1.50},
            {'nome': '🥥 Leite de Coco', 'preco': 1.80},
            
            # Açúcares
            {'nome': '🍯 Mel Encantado', 'preco': 1.20},
            {'nome': '🌵 Xarope de Agave', 'preco': 1.20},
            {'nome': '🚫 Sem Açúcar', 'preco': -0.50},
            
            # Especiarias
            {'nome': '🌿 Canela Encantada', 'preco': 1.00},
            {'nome': '🌰 Cardamomo Mágico', 'preco': 1.20},
            {'nome': '🌸 Essência de Baunilha', 'preco': 1.50},
            
            # Extras
            {'nome': '☁️ Chantilly das Nuvens', 'preco': 2.50},
            {'nome': '🤍 Marshmallows Mágicos', 'preco': 2.00},
            {'nome': '✨ Polvilho Dourado', 'preco': 1.00},
        ]
        for ingrediente_data in ingredientes_data:
            Ingrediente.objects.create(**ingrediente_data)

def home(request):
    """Página inicial do Expresso Patronum"""
    return render(request, 'menu/home.html')

def cardapio(request):
    """Exibe o cardápio completo com todas as bebidas"""
    # Criar dados iniciais se não existirem
    if not Cafe.objects.exists():
        _criar_dados_iniciais()
    
    cafes = Cafe.objects.all()
    chas = Cha.objects.all()
    ingredientes = Ingrediente.objects.all()
    
    # Dados completos das bebidas para o template
    bebidas_completas = [
        {
            'id': 'butterbeer',
            'nome': '🍺 Butterbeer Latte',
            'descricao': 'Café cremoso inspirado na famosa bebida de Hogwarts, com notas de caramelo, especiarias e uma pitada de magia dourada.',
            'preco': 12.50,
            'tipo': 'cafe',
            'casa': 'gryffindor',
            'ingredientes': ['☕ Espresso duplo encantado', '🥛 Leite vaporizado magicamente', '🍯 Xarope de caramelo mágico', '✨ Canela em pó encantada']
        },
        {
            'id': 'patronus',
            'nome': '🦌 Patronus Espresso',
            'descricao': 'Um espresso puro e poderoso que desperta sua energia interior, forte o suficiente para conjurar um Patronus.',
            'preco': 8.90,
            'tipo': 'cafe',
            'casa': 'gryffindor',
            'ingredientes': ['☕ Grãos selecionados de Hogwarts', '⚡ Energia mágica concentrada', '🍯 Açúcar cristalizado encantado']
        },
        {
            'id': 'biblioteca',
            'nome': '📚 Café da Biblioteca',
            'descricao': 'Para estudantes dedicados, um café que estimula a mente e a concentração, perfeito para longas sessões de estudo.',
            'preco': 11.20,
            'tipo': 'cafe',
            'casa': 'ravenclaw',
            'ingredientes': ['☕ Blend especial da Corvinal', '🧠 Essência da concentração', '📖 Aroma de pergaminho antigo']
        },
        {
            'id': 'mcgonagall',
            'nome': '🐱 Chá da Prof. McGonagall',
            'descricao': 'Um chá refinado e elegante, com blend de ervas especiais que acalma até mesmo o coração mais agitado.',
            'preco': 9.80,
            'tipo': 'cha',
            'casa': 'gryffindor',
            'ingredientes': ['🍵 Blend de ervas escocesas', '🌿 Hortelã do jardim de Hogwarts', '🍯 Mel encantado das abelhas mágicas', '🍋 Limão siciliano']
        },
        {
            'id': 'snape',
            'nome': '🐍 Poção do Professor Snape',
            'descricao': 'Um chá misterioso e complexo, com sabores profundos que revelam suas nuances lentamente.',
            'preco': 13.90,
            'tipo': 'cha',
            'casa': 'slytherin',
            'ingredientes': ['🌿 Ervas misteriosas da masmorra', '🌑 Essência de lua nova', '🐍 Toque de serpentina', '⚗️ Filtro da sabedoria']
        },
        {
            'id': 'firewhiskey',
            'nome': '🔥 Firewhiskey Coffee',
            'descricao': 'Uma bebida corajosa para momentos especiais, com um toque picante que aquece o coração.',
            'preco': 15.50,
            'tipo': 'especial',
            'casa': 'gryffindor',
            'ingredientes': ['🔥 Essência de firewhiskey', '☕ Café especial de Hogwarts', '🌶️ Pimenta encantada', '🍯 Mel dourado']
        },
        {
            'id': 'felicidade',
            'nome': '🧚 Elixir da Felicidade',
            'descricao': 'Uma bebida doce e reconfortante que traz alegria instantânea, perfeita para momentos que precisam de um pouquinho mais de magia.',
            'preco': 14.80,
            'tipo': 'especial',
            'casa': 'hufflepuff',
            'ingredientes': ['☕ Café doce das fadas', '🍓 Xarope de morango encantado', '🥛 Chantilly das nuvens', '✨ Polvilho mágico dourado']
        }
    ]
    
    context = {
        'bebidas': bebidas_completas,
        'cafes': cafes,
        'chas': chas,
        'ingredientes': ingredientes,
    }
    return render(request, 'menu/cardapio.html', context)

def personalizar(request, bebida_slug):
    """Página de personalização de bebidas usando padrão Decorator"""
    # Garantir que dados iniciais existam
    if not Ingrediente.objects.exists():
        _criar_dados_iniciais()
    
    # Mapear slugs para bebidas
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
        'biblioteca': {
            'nome': '📚 Café da Biblioteca',
            'descricao': 'Para estudantes dedicados, um café que estimula a mente e a concentração.',
            'preco': 11.20
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
    ingredientes = Ingrediente.objects.all()
    
    # Organizar ingredientes por categoria
    ingredientes_organizados = {
        'leites': ingredientes.filter(nome__contains='Leite'),
        'acucares': ingredientes.filter(nome__in=['🍯 Mel Encantado', '🌵 Xarope de Agave', '🚫 Sem Açúcar']),
        'especiarias': ingredientes.filter(nome__contains='Canela') | ingredientes.filter(nome__contains='Cardamomo') | ingredientes.filter(nome__contains='Baunilha'),
        'extras': ingredientes.filter(nome__in=['☁️ Chantilly das Nuvens', '🤍 Marshmallows Mágicos', '✨ Polvilho Dourado'])
    }
    
    context = {
        'bebida': bebida_info,
        'ingredientes': ingredientes,
        'ingredientes_organizados': ingredientes_organizados,
        'bebida_slug': bebida_slug,
    }
    return render(request, 'menu/personalizar.html', context)

def adicionar_ao_carrinho(request):
    """API para adicionar bebida personalizada ao carrinho usando padrão Decorator"""
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return JsonResponse({
            'success': False,
            'message': 'Você precisa estar logado para finalizar o pedido.',
            'redirect': '/menu/login/'
        })

    if request.method == 'POST':
        import json
        
        try:
            # Obter dados do POST
            bebida_slug = request.POST.get('bebida_slug')
            bebida_nome = request.POST.get('bebida_nome')
            preco_str = request.POST.get('bebida_preco', '0')
            preco_str = preco_str.replace(',', '.')
            bebida_preco = float(preco_str)
            leite_id = request.POST.get('leite')
            acucar_id = request.POST.get('acucar')
            ingredientes_ids = request.POST.getlist('ingredientes')
            observacoes = request.POST.get('observacoes', '')
            
            # Buscar bebida base
            bebida_base = None
            if bebida_slug in ['butterbeer', 'patronus', 'biblioteca', 'firewhiskey']:
                # É um café
                bebida_base = Cafe.objects.filter(nome__contains=bebida_nome.split(' ')[1]).first()
                if not bebida_base:
                    bebida_base = Cafe.objects.create(nome=bebida_nome, preco=bebida_preco)
            else:
                # É um chá
                bebida_base = Cha.objects.filter(nome__contains=bebida_nome.split(' ')[1]).first()
                if not bebida_base:
                    bebida_base = Cha.objects.create(nome=bebida_nome, preco=bebida_preco)
            
            # Aplicar padrão Decorator
            bebida_personalizada = BebidaPersonalizada(bebida_base)
            
            # Adicionar ingredientes
            if leite_id and leite_id != 'tradicional':
                leite = Ingrediente.objects.get(id=leite_id)
                bebida_personalizada.adicionar_ingrediente(leite)
            
            if acucar_id and acucar_id != 'normal':
                acucar = Ingrediente.objects.get(id=acucar_id)
                bebida_personalizada.adicionar_ingrediente(acucar)
            
            for ingrediente_id in ingredientes_ids:
                ingrediente = Ingrediente.objects.get(id=ingrediente_id)
                bebida_personalizada.adicionar_ingrediente(ingrediente)
            
            # Armazenar no carrinho da sessão
            if 'carrinho' not in request.session:
                request.session['carrinho'] = []

            item_carrinho = {
                'id': len(request.session['carrinho']) + 1,
                'bebida_nome': bebida_nome,
                'bebida_base_preco': float(bebida_base.preco),
                'descricao_completa': bebida_personalizada.descricao(),
                'preco_total': float(bebida_personalizada.get_preco()),
                'ingredientes': [ing.nome for ing in bebida_personalizada.ingredientes],
                'observacoes': observacoes
            }

            request.session['carrinho'].append(item_carrinho)
            request.session.modified = True

            # Adicionar pedido ao banco de dados (área Meus Pedidos)
            from pedido.commands import FazerPedidoCommand
            from pedido.models import PedidoBO
            cliente_nome = request.user.username if request.user.is_authenticated else 'Visitante'
            # Executa o comando para criar o pedido
            comando = FazerPedidoCommand(cliente_nome, bebida_personalizada, observacoes)
            comando.executar()

            return JsonResponse({
                'success': True,
                'message': 'Poção adicionada ao caldeirão com sucesso!',
                'item': item_carrinho,
                'total_carrinho': len(request.session['carrinho'])
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao adicionar poção: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

# --- Sistema de Login ---
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages

def login_view(request):
    """Redireciona para o sistema de login"""
    return redirect('auth:login_cliente')

def logout_view(request):
    """Redireciona para o novo sistema de logout"""
    return redirect('auth:logout')
