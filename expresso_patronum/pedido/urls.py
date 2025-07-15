from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.meus_pedidos, name='meus_pedidos'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('api/processar-pagamento/', views.processar_pagamento, name='processar_pagamento'),
    path('api/avancar-status/<int:pedido_id>/', views.avancar_status, name='avancar_status'),
    path('api/rastrear/<str:pedido_id>/', views.rastrear_pedido, name='rastrear_pedido'),
    
    # APIs para Command Pattern
    path('api/fazer-pedido/', views.api_fazer_pedido, name='api_fazer_pedido'),
    path('api/cancelar-pedido/<int:pedido_id>/', views.api_cancelar_pedido, name='api_cancelar_pedido'),
    path('api/alterar-pedido/<int:pedido_id>/', views.api_alterar_pedido, name='api_alterar_pedido'),
    path('api/desfazer/', views.api_desfazer_comando, name='api_desfazer'),
    path('api/refazer/', views.api_refazer_comando, name='api_refazer'),
    path('api/historico/', views.api_historico_comandos, name='api_historico'),
]
