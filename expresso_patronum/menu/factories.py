# Factory Method para criação de bebidas
from .models import Cafe, Cha

class BebidaFactory:
    """Factory Method para instanciar bebidas base"""
    
    @staticmethod
    def criar_bebida(tipo, nome, preco):
        """Cria uma bebida baseada no tipo especificado"""
        if tipo.lower() == 'cafe':
            bebida = Cafe(nome=nome, preco=preco)
        elif tipo.lower() == 'cha':
            bebida = Cha(nome=nome, preco=preco)
        else:
            raise ValueError(f"Tipo de bebida '{tipo}' não suportado")
        
        return bebida
    
    @staticmethod
    def criar_bebidas_padrao():
        """Cria as bebidas padrão do cardápio"""
        bebidas = [
            ('cafe', 'Butterbeer Latte', 12.50),
            ('cafe', 'Patronus Espresso', 8.90),
            ('cafe', 'Café da Biblioteca', 11.20),
            ('cafe', 'Firewhiskey Coffee', 15.50),
            ('cha', 'Chá da Prof. McGonagall', 9.80),
            ('cha', 'Poção do Professor Snape', 13.90),
            ('cafe', 'Elixir da Felicidade', 14.80),
        ]
        
        bebidas_criadas = []
        for tipo, nome, preco in bebidas:
            bebida = BebidaFactory.criar_bebida(tipo, nome, preco)
            bebidas_criadas.append(bebida)
        
        return bebidas_criadas
