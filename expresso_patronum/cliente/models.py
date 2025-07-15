from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Strategy Pattern: Diferentes tipos de fidelidade
class FidelityStrategy:
    def calcular_desconto(self, valor, pontos):
        return 0
    
    def calcular_pontos_ganhos(self, valor):
        return int(valor * 0.1)  # 1 ponto a cada R$ 10

class FidelityBronze(FidelityStrategy):
    def calcular_desconto(self, valor, pontos):
        if pontos >= 100:
            return valor * 0.05  # 5% de desconto
        return 0

class FidelityPrata(FidelityStrategy):
    def calcular_desconto(self, valor, pontos):
        if pontos >= 100:
            return valor * 0.10  # 10% de desconto
        return 0

class FidelityOuro(FidelityStrategy):
    def calcular_desconto(self, valor, pontos):
        if pontos >= 100:
            return valor * 0.15  # 15% de desconto
        return 0
    
    def calcular_pontos_ganhos(self, valor):
        return int(valor * 0.15)  # Pontos em dobro para ouro

# Perfil do Cliente
class ClienteProfile(models.Model):
    CASAS_CHOICES = [
        ('grifinoria', '🦁 Grifinória'),
        ('sonserina', '🐍 Sonserina'),
        ('corvinal', '🦅 Corvinal'),
        ('lufa_lufa', '🦡 Lufa-Lufa'),
    ]
    
    FIDELITY_LEVELS = [
        ('bronze', 'Bronze'),
        ('prata', 'Prata'),
        ('ouro', 'Ouro'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente_profile')
    casa_hogwarts = models.CharField(max_length=20, choices=CASAS_CHOICES, default='grifinoria')
    pontos_fidelidade = models.IntegerField(default=0)
    nivel_fidelidade = models.CharField(max_length=10, choices=FIDELITY_LEVELS, default='bronze')
    total_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pedidos_realizados = models.IntegerField(default=0)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    preferencias_bebida = models.TextField(blank=True, help_text="Preferências e observações sobre bebidas")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil do Cliente"
        verbose_name_plural = "Perfis dos Clientes"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_casa_hogwarts_display()}"
    
    def get_fidelity_strategy(self):
        """Retorna a estratégia de fidelidade baseada no nível"""
        strategies = {
            'bronze': FidelityBronze(),
            'prata': FidelityPrata(),
            'ouro': FidelityOuro(),
        }
        return strategies.get(self.nivel_fidelidade, FidelityBronze())
    
    def calcular_desconto(self, valor_pedido):
        """Calcula desconto baseado na estratégia de fidelidade"""
        strategy = self.get_fidelity_strategy()
        return strategy.calcular_desconto(valor_pedido, self.pontos_fidelidade)
    
    def adicionar_pontos(self, valor_pedido):
        """Adiciona pontos baseado no valor do pedido"""
        strategy = self.get_fidelity_strategy()
        novos_pontos = strategy.calcular_pontos_ganhos(valor_pedido)
        self.pontos_fidelidade += novos_pontos
        self.total_gasto += valor_pedido
        self.pedidos_realizados += 1
        
        # Atualizar nível de fidelidade
        self._atualizar_nivel_fidelidade()
        self.save()
        return novos_pontos
    
    def _atualizar_nivel_fidelidade(self):
        """Atualiza o nível de fidelidade baseado no total gasto"""
        if self.total_gasto >= 500:
            self.nivel_fidelidade = 'ouro'
        elif self.total_gasto >= 200:
            self.nivel_fidelidade = 'prata'
        else:
            self.nivel_fidelidade = 'bronze'
    
    def get_progresso_proximo_nivel(self):
        """Retorna o progresso para o próximo nível"""
        if self.nivel_fidelidade == 'bronze':
            return {
                'atual': float(self.total_gasto),
                'proximo': 200.0,
                'porcentagem': min((float(self.total_gasto) / 200.0) * 100, 100)
            }
        elif self.nivel_fidelidade == 'prata':
            return {
                'atual': float(self.total_gasto),
                'proximo': 500.0,
                'porcentagem': min((float(self.total_gasto) / 500.0) * 100, 100)
            }
        else:  # ouro
            return {
                'atual': float(self.total_gasto),
                'proximo': float(self.total_gasto),
                'porcentagem': 100
            }

@receiver(post_save, sender=User)
def create_or_update_cliente_profile(sender, instance, created, **kwargs):
    """Signal para criar perfil de cliente automaticamente"""
    # Só criar perfil se o usuário está no grupo de clientes ou não tem grupos ainda
    if created or instance.groups.filter(name='Clientes').exists():
        if not hasattr(instance, 'cliente_profile'):
            ClienteProfile.objects.create(user=instance)
        else:
            instance.cliente_profile.save()
