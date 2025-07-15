from django.core.management.base import BaseCommand
from menu.models import Cafe, Cha, Ingrediente

class Command(BaseCommand):
    help = 'Popular o banco de dados com bebidas e ingredientes do cardápio'

    def handle(self, *args, **options):
        self.stdout.write('🧙‍♂️ Populando o banco de dados com poções mágicas...')
        
        # Limpar dados existentes
        Cafe.objects.all().delete()
        Cha.objects.all().delete()
        Ingrediente.objects.all().delete()
        
        # Criar Cafés
        cafes = [
            {'nome': '🍺 Butterbeer Latte', 'preco': 12.50},
            {'nome': '🦌 Patronus Espresso', 'preco': 8.90},
            {'nome': '📚 Café da Biblioteca', 'preco': 11.20},
            {'nome': '🔥 Firewhiskey Coffee', 'preco': 15.50},
        ]
        
        for cafe_data in cafes:
            cafe = Cafe.objects.create(**cafe_data)
            self.stdout.write(f'✅ Criado café: {cafe.nome}')
        
        # Criar Chás
        chas = [
            {'nome': '🐱 Chá da Prof. McGonagall', 'preco': 9.80},
            {'nome': '🐍 Poção do Professor Snape', 'preco': 13.90},
        ]
        
        for cha_data in chas:
            cha = Cha.objects.create(**cha_data)
            self.stdout.write(f'✅ Criado chá: {cha.nome}')
        
        # Criar Ingredientes
        ingredientes = [
            # Leites
            {'nome': '🥛 Leite de Aveia', 'preco': 1.50},
            {'nome': '🌰 Leite de Amêndoas', 'preco': 1.50},
            {'nome': '🥥 Leite de Coco', 'preco': 1.80},
            {'nome': '🐄 Leite Tradicional', 'preco': 0.00},
            
            # Açúcares
            {'nome': '🍯 Mel Encantado', 'preco': 1.20},
            {'nome': '🌵 Xarope de Agave', 'preco': 1.20},
            {'nome': '🚫 Sem Açúcar', 'preco': -0.50},
            
            # Especiarias
            {'nome': '🌿 Canela Encantada', 'preco': 1.00},
            {'nome': '🌰 Cardamomo Mágico', 'preco': 1.20},
            {'nome': '🌸 Essência de Baunilha', 'preco': 1.50},
            {'nome': '🥜 Noz-moscada Encantada', 'preco': 1.00},
            {'nome': '🫚 Gengibre Mágico', 'preco': 0.80},
            {'nome': '🍫 Chocolate Amargo', 'preco': 2.00},
            
            # Extras
            {'nome': '☁️ Chantilly das Nuvens', 'preco': 2.50},
            {'nome': '🤍 Marshmallows Mágicos', 'preco': 2.00},
            {'nome': '🍯 Calda de Caramelo', 'preco': 1.80},
            {'nome': '✨ Polvilho Dourado', 'preco': 1.00},
        ]
        
        for ingrediente_data in ingredientes:
            ingrediente = Ingrediente.objects.create(**ingrediente_data)
            self.stdout.write(f'✅ Criado ingrediente: {ingrediente.nome}')
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Banco de dados populado com sucesso!')
        )
