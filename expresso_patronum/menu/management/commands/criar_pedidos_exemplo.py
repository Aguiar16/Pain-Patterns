from django.core.management.base import BaseCommand
from pedido.models import Pedido
from menu.models import Cafe, Cha, Ingrediente
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Cria pedidos de exemplo para demonstração'

    def handle(self, *args, **options):
        self.stdout.write('🧙‍♂️ Criando pedidos de exemplo...')
        
        # Criar alguns ingredientes se não existirem
        if not Ingrediente.objects.exists():
            ingredientes_data = [
                {'nome': '🥛 Leite de Aveia', 'preco': 1.50},
                {'nome': '🌿 Canela Encantada', 'preco': 1.00},
                {'nome': '☁️ Chantilly das Nuvens', 'preco': 2.50},
                {'nome': '🍯 Mel Encantado', 'preco': 1.20},
            ]
            for ingrediente_data in ingredientes_data:
                Ingrediente.objects.create(**ingrediente_data)
        
        # Criar algumas bebidas se não existirem
        if not Cafe.objects.exists():
            cafes_data = [
                {'nome': '🍺 Butterbeer Latte', 'preco': 12.50},
                {'nome': '🦌 Patronus Espresso', 'preco': 8.90},
            ]
            for cafe_data in cafes_data:
                Cafe.objects.create(**cafe_data)
        
        if not Cha.objects.exists():
            chas_data = [
                {'nome': '🐱 Chá da Prof. McGonagall', 'preco': 9.80},
                {'nome': '🐍 Poção do Professor Snape', 'preco': 13.90},
            ]
            for cha_data in chas_data:
                Cha.objects.create(**cha_data)
        
        # Limpar pedidos existentes
        Pedido.objects.all().delete()
        
        # Criar pedidos de exemplo
        clientes = ['Harry Potter', 'Hermione Granger', 'Ron Weasley', 'Luna Lovegood', 'Draco Malfoy', 'Neville Longbottom']
        bebidas = [
            '🍺 Butterbeer Latte com Leite de Aveia e Canela',
            '🦌 Patronus Espresso Duplo',
            '🐱 Chá da Prof. McGonagall com Mel',
            '🐍 Poção do Professor Snape Especial',
            '🔥 Firewhiskey Coffee com Chantilly',
            '🧚 Elixir da Felicidade'
        ]
        status_opcoes = ['Recebido', 'Em preparo', 'Pronto', 'Entregue']
        precos = [8.90, 12.50, 15.50, 9.80, 13.90, 14.80]
        
        # Criar 15 pedidos com diferentes status e horários
        import datetime
        for i in range(15):
            # Horários variados nas últimas 4 horas
            horas_atras = random.randint(0, 240)  # até 4 horas atrás
            data_criacao = timezone.now() - datetime.timedelta(minutes=horas_atras)
            
            # Status baseado no tempo (mais antigos têm maior chance de estar prontos)
            if horas_atras > 120:  # Mais de 2 horas
                status = random.choice(['Pronto', 'Entregue'])
            elif horas_atras > 60:  # Mais de 1 hora
                status = random.choice(['Em preparo', 'Pronto'])
            else:  # Últimos 60 minutos
                status = random.choice(['Recebido', 'Em preparo'])
            
            pedido = Pedido.objects.create(
                cliente=random.choice(clientes),
                bebida=random.choice(bebidas),
                preco=random.choice(precos),
                status=status,
                criado_em=data_criacao
            )
            
            self.stdout.write(f'✅ Criado pedido #{str(pedido.id).zfill(3)}: {pedido.bebida} - {pedido.cliente} ({pedido.status})')
        
        # Estatísticas
        total_pedidos = Pedido.objects.count()
        recebidos = Pedido.objects.filter(status='Recebido').count()
        em_preparo = Pedido.objects.filter(status='Em preparo').count()
        prontos = Pedido.objects.filter(status='Pronto').count()
        entregues = Pedido.objects.filter(status='Entregue').count()
        
        self.stdout.write(
            self.style.SUCCESS(f'''
🎉 Pedidos criados com sucesso!

📊 Estatísticas:
- Total: {total_pedidos}
- Recebidos: {recebidos}
- Em preparo: {em_preparo}
- Prontos: {prontos}
- Entregues: {entregues}

Agora você pode testar o painel da cozinha!
''')
        )
