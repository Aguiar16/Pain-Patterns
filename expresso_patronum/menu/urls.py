from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('cardapio/', views.cardapio, name='cardapio'),
    path('personalizar/<slug:bebida_slug>/', views.personalizar, name='personalizar'),
    path('api/adicionar-carrinho/', views.adicionar_ao_carrinho, name='adicionar_carrinho'),
]
