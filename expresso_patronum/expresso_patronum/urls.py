"""
URL configuration for expresso_patronum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views.menu_view import menu
from views.carrinho_view import carrinho
from views.pagamento_view import pagamento
from views.cozinha_view import cozinha
from views.status_view import status_pedido

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu, name='home'),
    path('menu/', menu, name='menu'),
    path('carrinho/', carrinho, name='carrinho'),
    path('pagamento/', pagamento, name='pagamento'),
    path('cozinha/', cozinha, name='cozinha'),
    path('status/', status_pedido, name='status_pedido'),
]
