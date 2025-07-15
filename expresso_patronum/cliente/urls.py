from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('historico/', views.historico, name='historico'),
    path('api/atualizar-perfil/', views.atualizar_perfil, name='atualizar_perfil'),
    path('api/estatisticas-dinamicas/', views.api_estatisticas_dinamicas, name='api_estatisticas_dinamicas'),
]
