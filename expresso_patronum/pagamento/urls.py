from django.urls import path
from . import views

app_name = 'pagamento'

urlpatterns = [
    path('api/calcular-desconto/', views.calcular_desconto, name='calcular_desconto'),
    path('api/sugerir-descontos/', views.sugerir_descontos, name='sugerir_descontos'),
]
