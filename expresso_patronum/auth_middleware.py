"""
Middleware para inicializar automaticamente o sistema de autenticação
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger(__name__)

class AuthSystemMiddleware(MiddlewareMixin):
    """Middleware que garante que o sistema de autenticação está configurado"""
    
    _initialized = False
    
    def process_request(self, request):
        """Verifica e inicializa o sistema de autenticação se necessário"""
        if not AuthSystemMiddleware._initialized:
            try:
                # Verificar se os grupos existem
                if not Group.objects.filter(name='Clientes').exists():
                    from auth_system import initialize_auth_system
                    initialize_auth_system()
                    logger.info("Sistema de autenticação inicializado automaticamente")
                
                AuthSystemMiddleware._initialized = True
                
            except Exception as e:
                logger.error(f"Erro ao inicializar sistema de autenticação: {e}")
        
        return None
