from django.urls import path
from auth_system import (
    login_cliente, register_cliente,
    logout_view, profile_redirect, manage_users, toggle_user_status
)

app_name = 'auth'

urlpatterns = [
    # Login/Logout
    path('login/', login_cliente, name='login_cliente'),
    path('login/cliente/', login_cliente, name='login_cliente'),  # Alias para compatibilidade
    path('register/cliente/', register_cliente, name='register_cliente'),
    path('logout/', logout_view, name='logout'),
    
    # Redirecionamento
    path('profile/', profile_redirect, name='profile_redirect'),
    
    # Gerenciamento (Admin apenas)
    path('manage/users/', manage_users, name='manage_users'),
    path('api/toggle-user-status/', toggle_user_status, name='toggle_user_status'),
]
