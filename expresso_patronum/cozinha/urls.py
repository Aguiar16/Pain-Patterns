from django.urls import path
from . import views

app_name = 'cozinha'

urlpatterns = [
    path('', views.painel, name='painel'),
    path('api/iniciar-preparo/<str:pedido_id>/', views.iniciar_preparo, name='iniciar_preparo'),
    path('api/marcar-pronto/<str:pedido_id>/', views.marcar_pronto, name='marcar_pronto'),
    path('api/marcar-entregue/<str:pedido_id>/', views.marcar_entregue, name='marcar_entregue'),
    path('api/estatisticas/', views.estatisticas, name='estatisticas'),
]
