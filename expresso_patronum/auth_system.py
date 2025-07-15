"""
Sistema de autenticação robusto para o Expresso Patronum
Separação entre clientes e funcionários da cozinha
"""

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# ========================= DECORADORES DE AUTENTICAÇÃO =========================

def cliente_required(view_func):
    """Decorator que verifica se o usuário é um cliente"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa fazer login como cliente para acessar esta página.')
            return redirect('auth:login_cliente')
        
        if not hasattr(request.user, 'cliente_profile') and not request.user.groups.filter(name='Clientes').exists():
            messages.error(request, 'Acesso negado. Esta área é restrita a clientes.')
            return redirect('menu:home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    """Decorator que verifica se o usuário é admin"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Login necessário.')
            return redirect('auth:login_cliente')
        
        if not request.user.is_staff:
            messages.error(request, 'Acesso negado. Área restrita a administradores.')
            return redirect('menu:home')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# ========================= FUNÇÕES AUXILIARES =========================

def is_cliente(user):
    """Verifica se o usuário é um cliente"""
    return (hasattr(user, 'cliente_profile') or 
            user.groups.filter(name='Clientes').exists())

def is_admin(user):
    """Verifica se o usuário é um administrador"""
    return user.is_staff or user.is_superuser

def setup_groups_and_permissions():
    """Configura grupos e permissões iniciais"""
    try:
        # Criar grupo de clientes se não existir
        clientes_group, created = Group.objects.get_or_create(name='Clientes')
        
        # Configurar permissões específicas
        from django.contrib.contenttypes.models import ContentType
        from pedido.models import Pedido
        
        pedido_content_type = ContentType.objects.get_for_model(Pedido)
        
        # Permissões para clientes
        view_own_pedido, created = Permission.objects.get_or_create(
            codename='view_own_pedido',
            name='Can view own pedidos',
            content_type=pedido_content_type,
        )
        
        add_pedido_perm = Permission.objects.get(
            codename='add_pedido',
            content_type=pedido_content_type,
        )
        
        clientes_group.permissions.set([view_own_pedido, add_pedido_perm])
        
        logger.info("Grupos e permissões configurados com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao configurar grupos e permissões: {e}")

# ========================= VIEWS DE AUTENTICAÇÃO =========================

@require_http_methods(["GET", "POST"])
def login_cliente(request):
    """View de login específica para clientes"""
    if request.user.is_authenticated:
        if is_cliente(request.user):
            return redirect('cliente:perfil')
        elif request.user.is_staff:
            return redirect('cozinha:painel')
        else:
            django_logout(request)
            messages.info(request, 'Você foi deslogado. Faça login novamente.')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'auth/login_cliente.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # Verificar se é admin
                if user.is_staff:
                    django_login(request, user)
                    messages.success(request, f'Bem-vindo, Administrador {user.first_name or user.username}!')
                    return redirect('cozinha:painel')
                
                # Adicionar ao grupo de clientes se não for admin
                if not is_cliente(user):
                    clientes_group = Group.objects.get(name='Clientes')
                    user.groups.add(clientes_group)
                
                django_login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.first_name or user.username}!')
                
                # Redirect para próxima página ou perfil
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('cliente:perfil')
            else:
                messages.error(request, 'Conta desativada. Entre em contato com o suporte.')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'auth/login_cliente.html')

@login_required
def logout_view(request):
    """View de logout universal"""
    user_name = request.user.first_name or request.user.username
    was_admin = request.user.is_staff
    
    django_logout(request)
    messages.success(request, f'Logout realizado com sucesso, {user_name}!')
    
    # Redirect baseado no tipo de usuário
    if was_admin:
        return redirect('auth:login_cliente')
    else:
        return redirect('menu:home')

@login_required
def profile_redirect(request):
    """Redireciona para o perfil apropriado baseado no tipo de usuário"""
    if request.user.is_staff:
        return redirect('cozinha:painel')
    elif is_cliente(request.user):
        return redirect('cliente:perfil')
    else:
        messages.error(request, 'Tipo de usuário não identificado.')
        return redirect('menu:home')

# ========================= VIEWS DE GERENCIAMENTO =========================

@admin_required
def manage_users(request):
    """View para gerenciar usuários (admin apenas)"""
    clientes = User.objects.filter(groups__name='Clientes').order_by('date_joined')
    
    context = {
        'clientes': clientes,
        'total_clientes': clientes.count(),
    }
    
    return render(request, 'auth/manage_users.html', context)

@require_http_methods(["POST"])
@admin_required
def toggle_user_status(request):
    """API para ativar/desativar usuários"""
    try:
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Não permitir desativar o próprio usuário
        if user == request.user:
            return JsonResponse({
                'success': False, 
                'message': 'Você não pode desativar sua própria conta.'
            })
        
        user.is_active = not user.is_active
        user.save()
        
        status = 'ativado' if user.is_active else 'desativado'
        return JsonResponse({
            'success': True,
            'message': f'Usuário {user.username} foi {status}.',
            'is_active': user.is_active
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Usuário não encontrado.'
        })
    except Exception as e:
        logger.error(f"Erro ao alterar status do usuário: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Erro interno do servidor.'
        })

# ========================= REGISTRO DE CLIENTE =========================

@require_http_methods(["GET", "POST"])
def register_cliente(request):
    """View de registro para novos clientes"""
    if request.user.is_authenticated:
        return redirect('cliente:perfil')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validações
        if not all([username, email, first_name, password, password_confirm]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'auth/register_cliente.html')
        
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'auth/register_cliente.html')
        
        if len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'auth/register_cliente.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe. Escolha outro.')
            return render(request, 'auth/register_cliente.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return render(request, 'auth/register_cliente.html')
        
        try:
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Adicionar ao grupo de clientes
            clientes_group = Group.objects.get(name='Clientes')
            user.groups.add(clientes_group)
            
            # Login automático
            django_login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {first_name}!')
            return redirect('cliente:perfil')
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            messages.error(request, 'Erro interno. Tente novamente.')
    
    return render(request, 'auth/register_cliente.html')

# ========================= INICIALIZAÇÃO =========================

def initialize_auth_system():
    """Inicializa o sistema de autenticação"""
    try:
        setup_groups_and_permissions()
        logger.info("Sistema de autenticação inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema de autenticação: {e}")
