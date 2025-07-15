# Command Pattern para operações de pedido
from abc import ABC, abstractmethod
from .models import Pedido, PedidoDAO, PedidoBO
from cozinha.models import CozinhaObserver, ClienteObserver

class PedidoCommand(ABC):
    """Interface base para comandos de pedido"""
    
    @abstractmethod
    def executar(self):
        pass
    
    @abstractmethod
    def desfazer(self):
        pass

class FazerPedidoCommand(PedidoCommand):
    """Comando para fazer um novo pedido"""
    
    def __init__(self, cliente, bebida_personalizada, observacoes=None):
        self.cliente = cliente
        self.bebida_personalizada = bebida_personalizada
        self.observacoes = observacoes
        self.pedido_criado = None
        self.historico = []
    
    def executar(self):
        """Executa a criação do pedido"""
        try:
            # Criar o pedido usando BO
            self.pedido_criado = PedidoBO.criar_pedido(
                self.cliente, 
                self.bebida_personalizada
            )
            
            # Adicionar observações se fornecidas
            if self.observacoes:
                self.pedido_criado.observacoes = self.observacoes
                self.pedido_criado.save()
            
            # Adicionar observadores
            self.pedido_criado.adicionar_observador(CozinhaObserver())
            self.pedido_criado.adicionar_observador(ClienteObserver(self.cliente))
            
            # Notificar observadores
            self.pedido_criado.notificar_observadores()
            
            # Salvar no histórico para possível desfazer
            self.historico.append({
                'acao': 'criar',
                'pedido_id': self.pedido_criado.id,
                'estado_anterior': None
            })
            
            return {
                'success': True,
                'pedido': self.pedido_criado,
                'message': f'Pedido #{self.pedido_criado.id} criado com sucesso!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao criar pedido: {str(e)}'
            }
    
    def desfazer(self):
        """Desfaz a criação do pedido"""
        if self.pedido_criado:
            try:
                pedido_id = self.pedido_criado.id
                self.pedido_criado.delete()
                self.pedido_criado = None
                
                return {
                    'success': True,
                    'message': f'Pedido #{pedido_id} cancelado com sucesso!'
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Erro ao cancelar pedido: {str(e)}'
                }
        
        return {
            'success': False,
            'message': 'Nenhum pedido para cancelar'
        }

class CancelarPedidoCommand(PedidoCommand):
    """Comando para cancelar um pedido existente"""
    
    def __init__(self, pedido_id, motivo=None):
        self.pedido_id = pedido_id
        self.motivo = motivo
        self.pedido_original = None
        self.estado_anterior = None
        self.historico = []
    
    def executar(self):
        """Executa o cancelamento do pedido"""
        try:
            # Buscar o pedido
            self.pedido_original = PedidoDAO.buscar_por_id(self.pedido_id)
            
            # Verificar se pode ser cancelado
            if self.pedido_original.status in ['Entregue']:
                return {
                    'success': False,
                    'message': 'Não é possível cancelar um pedido já entregue'
                }
            
            # Salvar estado anterior para possível desfazer
            self.estado_anterior = {
                'status': self.pedido_original.status,
                'observacoes': getattr(self.pedido_original, 'observacoes', '')
            }
            
            # Atualizar status para cancelado
            self.pedido_original.status = 'Cancelado'
            if self.motivo:
                observacoes_atuais = getattr(self.pedido_original, 'observacoes', '')
                self.pedido_original.observacoes = f"{observacoes_atuais}\n[CANCELADO] Motivo: {self.motivo}"
            
            # Salvar alterações
            PedidoDAO.salvar(self.pedido_original)
            
            # Notificar observadores sobre o cancelamento
            self.pedido_original.adicionar_observador(CozinhaObserver())
            self.pedido_original.adicionar_observador(ClienteObserver(self.pedido_original.cliente))
            self.pedido_original.notificar_observadores()
            
            # Salvar no histórico
            self.historico.append({
                'acao': 'cancelar',
                'pedido_id': self.pedido_id,
                'estado_anterior': self.estado_anterior
            })
            
            return {
                'success': True,
                'message': f'Pedido #{self.pedido_id} cancelado com sucesso!'
            }
            
        except Pedido.DoesNotExist:
            return {
                'success': False,
                'message': f'Pedido #{self.pedido_id} não encontrado'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao cancelar pedido: {str(e)}'
            }
    
    def desfazer(self):
        """Desfaz o cancelamento do pedido"""
        if self.pedido_original and self.estado_anterior:
            try:
                # Restaurar estado anterior
                self.pedido_original.status = self.estado_anterior['status']
                self.pedido_original.observacoes = self.estado_anterior['observacoes']
                
                # Salvar alterações
                PedidoDAO.salvar(self.pedido_original)
                
                # Notificar observadores
                self.pedido_original.notificar_observadores()
                
                return {
                    'success': True,
                    'message': f'Cancelamento do pedido #{self.pedido_id} foi desfeito!'
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Erro ao desfazer cancelamento: {str(e)}'
                }
        
        return {
            'success': False,
            'message': 'Nenhum cancelamento para desfazer'
        }

class AlterarPedidoCommand(PedidoCommand):
    """Comando para alterar um pedido existente"""
    
    def __init__(self, pedido_id, nova_bebida_personalizada=None, novo_cliente=None, novas_observacoes=None):
        self.pedido_id = pedido_id
        self.nova_bebida_personalizada = nova_bebida_personalizada
        self.novo_cliente = novo_cliente
        self.novas_observacoes = novas_observacoes
        self.pedido_original = None
        self.estado_anterior = None
        self.historico = []
    
    def executar(self):
        """Executa a alteração do pedido"""
        try:
            # Buscar o pedido
            self.pedido_original = PedidoDAO.buscar_por_id(self.pedido_id)
            
            # Verificar se pode ser alterado
            if self.pedido_original.status in ['Entregue', 'Cancelado']:
                return {
                    'success': False,
                    'message': 'Não é possível alterar um pedido entregue ou cancelado'
                }
            
            if self.pedido_original.status == 'Em preparo':
                return {
                    'success': False,
                    'message': 'Pedido já está em preparo. Cancelamento pode ser necessário.'
                }
            
            # Salvar estado anterior para possível desfazer
            self.estado_anterior = {
                'cliente': self.pedido_original.cliente,
                'bebida': self.pedido_original.bebida,
                'preco': float(self.pedido_original.preco),
                'observacoes': getattr(self.pedido_original, 'observacoes', '')
            }
            
            alteracoes = []
            
            # Aplicar alterações
            if self.nova_bebida_personalizada:
                self.pedido_original.bebida = self.nova_bebida_personalizada.descricao()
                self.pedido_original.preco = self.nova_bebida_personalizada.get_preco()
                alteracoes.append('bebida personalizada')
            
            if self.novo_cliente:
                self.pedido_original.cliente = self.novo_cliente
                alteracoes.append('cliente')
            
            if self.novas_observacoes is not None:
                self.pedido_original.observacoes = self.novas_observacoes
                alteracoes.append('observações')
            
            # Salvar alterações
            PedidoDAO.salvar(self.pedido_original)
            
            # Notificar observadores sobre a alteração
            self.pedido_original.adicionar_observador(CozinhaObserver())
            self.pedido_original.adicionar_observador(ClienteObserver(self.pedido_original.cliente))
            self.pedido_original.notificar_observadores()
            
            # Salvar no histórico
            self.historico.append({
                'acao': 'alterar',
                'pedido_id': self.pedido_id,
                'estado_anterior': self.estado_anterior,
                'alteracoes': alteracoes
            })
            
            return {
                'success': True,
                'message': f'Pedido #{self.pedido_id} alterado com sucesso! Alterações: {", ".join(alteracoes)}'
            }
            
        except Pedido.DoesNotExist:
            return {
                'success': False,
                'message': f'Pedido #{self.pedido_id} não encontrado'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao alterar pedido: {str(e)}'
            }
    
    def desfazer(self):
        """Desfaz a alteração do pedido"""
        if self.pedido_original and self.estado_anterior:
            try:
                # Restaurar estado anterior
                self.pedido_original.cliente = self.estado_anterior['cliente']
                self.pedido_original.bebida = self.estado_anterior['bebida']
                self.pedido_original.preco = self.estado_anterior['preco']
                self.pedido_original.observacoes = self.estado_anterior['observacoes']
                
                # Salvar alterações
                PedidoDAO.salvar(self.pedido_original)
                
                # Notificar observadores
                self.pedido_original.notificar_observadores()
                
                return {
                    'success': True,
                    'message': f'Alterações do pedido #{self.pedido_id} foram desfeitas!'
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Erro ao desfazer alteração: {str(e)}'
                }
        
        return {
            'success': False,
            'message': 'Nenhuma alteração para desfazer'
        }

class InvokerPedidos:
    """Invoker para gerenciar comandos de pedido e histórico de desfazer/refazer"""
    
    def __init__(self):
        self.historico_comandos = []
        self.indice_atual = -1
    
    def executar_comando(self, comando):
        """Executa um comando e adiciona ao histórico"""
        resultado = comando.executar()
        
        if resultado.get('success', False):
            # Remove comandos após o índice atual (para casos de redo)
            self.historico_comandos = self.historico_comandos[:self.indice_atual + 1]
            
            # Adiciona o novo comando
            self.historico_comandos.append(comando)
            self.indice_atual += 1
        
        return resultado
    
    def desfazer(self):
        """Desfaz o último comando executado"""
        if self.indice_atual >= 0:
            comando = self.historico_comandos[self.indice_atual]
            resultado = comando.desfazer()
            
            if resultado.get('success', False):
                self.indice_atual -= 1
            
            return resultado
        
        return {
            'success': False,
            'message': 'Nenhum comando para desfazer'
        }
    
    def refazer(self):
        """Refaz o próximo comando no histórico"""
        if self.indice_atual < len(self.historico_comandos) - 1:
            self.indice_atual += 1
            comando = self.historico_comandos[self.indice_atual]
            return comando.executar()
        
        return {
            'success': False,
            'message': 'Nenhum comando para refazer'
        }
    
    def obter_historico(self):
        """Retorna o histórico de comandos executados"""
        return [
            {
                'tipo': type(cmd).__name__,
                'executado': i <= self.indice_atual
            }
            for i, cmd in enumerate(self.historico_comandos)
        ]
