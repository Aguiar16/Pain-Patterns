"""
Script de inicialização do sistema de autenticação robusto
Execute após as migrações para configurar grupos e permissões
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expresso_patronum.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from cliente.models import ClienteProfile
from auth_system import initialize_auth_system
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_demo_users():
    """Cria usuários de demonstração"""
    logger.info("Criando usuários de demonstração...")
    
    # Usuário cliente genérico
    cliente_data = {
        'username': 'client',
        'email': 'client@expressopatronum.com',
        'first_name': 'Cliente',
        'last_name': 'Genérico',
        'password': 'client123',
        'casa': 'grifinoria',
        'pontos': 50
    }
    
    clientes_group = Group.objects.get(name='Clientes')
    
    username = cliente_data['username']
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=cliente_data['email'],
            password=cliente_data['password'],
            first_name=cliente_data['first_name'],
            last_name=cliente_data['last_name']
        )
        
        user.groups.add(clientes_group)
        
        # Criar perfil de cliente se não existir
        cliente_profile, created = ClienteProfile.objects.get_or_create(
            user=user,
            defaults={
                'casa_hogwarts': cliente_data['casa'],
                'pontos_fidelidade': cliente_data['pontos'],
                'nivel_fidelidade': 'bronze'
            }
        )
        
        logger.info(f"Cliente criado: {username}")

def create_admin_user():
    """Cria usuário administrador"""
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@expressopatronum.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema'
        )
        
        # Adicionar ao grupo de clientes também (para testes)
        clientes_group = Group.objects.get(name='Clientes')
        admin.groups.add(clientes_group)
        
        logger.info("Usuário administrador criado: admin/admin123")

def main():
    """Função principal de inicialização"""
    try:
        logger.info("=== Inicializando Sistema de Autenticação Robusto ===")
        
        # Configurar grupos e permissões
        initialize_auth_system()
        
        # Criar usuários de demonstração
        create_demo_users()
        
        # Criar usuário admin
        create_admin_user()
        
        logger.info("=== Sistema de Autenticação Inicializado com Sucesso ===")
        logger.info("\nUsuários criados:")
        logger.info("CLIENTE:")
        logger.info("  client / client123")
        logger.info("\nADMINISTRADOR:")
        logger.info("  admin / admin123")
        logger.info("\nURLs de Login:")
        logger.info("  Login: /auth/login/")
        logger.info("  Registro: /auth/register/cliente/")
        logger.info("  Painel Admin: /cozinha/painel/ (apenas admin)")
        
    except Exception as e:
        logger.error(f"Erro durante a inicialização: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
