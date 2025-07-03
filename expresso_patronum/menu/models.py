from django.db import models

# Factory Method: Classe abstrata para bebidas base
class BebidaBase(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        abstract = True

    def descricao(self):
        return self.nome

    def get_preco(self):
        return self.preco

# Factory Method: Implementações concretas
class Cafe(BebidaBase):
    pass

class Cha(BebidaBase):
    pass

# Ingredientes opcionais (Decorator)
class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

# Decorator: Classe para compor bebidas personalizadas
class BebidaPersonalizada:
    def __init__(self, bebida_base):
        self.bebida_base = bebida_base
        self.ingredientes = []

    def adicionar_ingrediente(self, ingrediente):
        self.ingredientes.append(ingrediente)

    def descricao(self):
        desc = self.bebida_base.descricao()
        if self.ingredientes:
            desc += ' com ' + ', '.join([i.nome for i in self.ingredientes])
        return desc

    def get_preco(self):
        total = self.bebida_base.get_preco()
        total += sum([i.preco for i in self.ingredientes])
        return total
