from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('historico/', views.historico, name='historico'),
]
