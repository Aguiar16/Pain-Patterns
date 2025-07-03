from django.core.management.base import BaseCommand
from menu.models import Ingrediente
from menu.factories import BebidaFactory

class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais do Expresso Patronum'

    def handle(self, *args, **options):
        self.stdout.write('🧙‍♂️ Criando dados mágicos...')
        
        # Criar ingredientes
        ingredientes_data = [
            ('Leite de Aveia', 1.50),
            ('Leite de Amêndoas', 1.50),
            ('Leite de Coco', 1.50),
            ('Açúcar Cristal', 0.50),
            ('Mel de Abelhas Mágicas', 1.00),
            ('Xarope de Agave', 1.20),
            ('Canela Encantada', 1.00),
            ('Cardamomo Mágico', 1.20),
            ('Essência de Baunilha', 1.50),
            ('Noz-moscada Encantada', 1.00),
            ('Gengibre Mágico', 0.80),
            ('Chocolate Amargo', 2.00),
            ('Chantilly das Nuvens', 2.50),
            ('Marshmallows Mágicos', 2.00),
            ('Calda de Caramelo', 1.80),
            ('Polvilho Dourado', 1.00),
        ]
        
        for nome, preco in ingredientes_data:
            ingrediente, created = Ingrediente.objects.get_or_create(
                nome=nome,
                defaults={'preco': preco}
            )
            if created:
                self.stdout.write(f'✨ Criado ingrediente: {nome}')
        
        # Criar bebidas usando Factory Method
        try:
            bebidas = BebidaFactory.criar_bebidas_padrao()
            for bebida in bebidas:
                bebida.save()
                self.stdout.write(f'🍺 Criada bebida: {bebida.nome}')
        except Exception as e:
            self.stdout.write(f'⚠️ Bebidas podem já existir: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Dados mágicos criados com sucesso!')
        )
