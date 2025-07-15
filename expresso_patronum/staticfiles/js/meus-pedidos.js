// JavaScript para a página Meus Pedidos (Carrinho)

class CarrinhoManager {
    constructor() {
        this.itens = [];
        this.init();
    }

    init() {
        this.carregarCarrinho();
        this.sincronizarComSessao(); // Sincronizar com sessão se houver
        this.setupEventListeners();
        this.atualizarInterface();
    }

    carregarCarrinho() {
        // Carregar itens do localStorage ou sessionStorage
        const savedItems = localStorage.getItem('carrinho_expresso');
        if (savedItems) {
            this.itens = JSON.parse(savedItems);
        }
    }

    salvarCarrinho() {
        localStorage.setItem('carrinho_expresso', JSON.stringify(this.itens));
    }

    adicionarItem(bebida, preco, ingredientes = []) {
        const item = {
            id: Date.now(),
            bebida,
            preco: parseFloat(preco),
            quantidade: 1,
            ingredientes,
            observacoes: '',
            personalizada: false
        };
        this.itens.push(item);
        this.salvarCarrinho();
        this.atualizarInterface();
        showMagicalNotification(`✨ ${bebida} adicionado ao carrinho!`, 'success');
    }

    adicionarItemPersonalizado(itemPersonalizado) {
        // Verificar se já existe um item igual
        const itemExistente = this.itens.find(item => 
            item.bebida === itemPersonalizado.bebida && 
            item.personalizada === true &&
            JSON.stringify(item.ingredientes) === JSON.stringify(itemPersonalizado.ingredientes)
        );

        if (itemExistente) {
            // Se existe, aumentar quantidade
            itemExistente.quantidade += 1;
            showMagicalNotification(`✨ Quantidade de ${itemPersonalizado.bebida} aumentada!`, 'success');
        } else {
            // Se não existe, adicionar novo item
            const novoItem = {
                ...itemPersonalizado,
                id: Date.now(),
                personalizada: true
            };
            this.itens.push(novoItem);
            showMagicalNotification(`✨ ${itemPersonalizado.bebida} personalizada adicionada ao carrinho!`, 'success');
        }
        
        this.salvarCarrinho();
        this.atualizarInterface();
    }

    removerItem(itemId) {
        this.itens = this.itens.filter(item => item.id !== itemId);
        this.salvarCarrinho();
        this.atualizarInterface();
        showMagicalNotification('Item removido do carrinho! 🗑️', 'info');
    }

    atualizarQuantidade(itemId, novaQuantidade) {
        if (novaQuantidade <= 0) {
            this.removerItem(itemId);
            return;
        }

        const item = this.itens.find(item => item.id === itemId);
        if (item) {
            item.quantidade = novaQuantidade;
            this.salvarCarrinho();
            this.atualizarInterface();
        }
    }

    atualizarObservacoes(itemId, observacoes) {
        const item = this.itens.find(item => item.id === itemId);
        if (item) {
            item.observacoes = observacoes;
            this.salvarCarrinho();
        }
    }

    calcularTotal() {
        return this.itens.reduce((total, item) => total + (item.preco * item.quantidade), 0);
    }

    limparCarrinho() {
        this.itens = [];
        this.salvarCarrinho();
        this.atualizarInterface();
        showMagicalNotification('Carrinho limpo! 🧹', 'info');
    }

    atualizarInterface() {
        this.renderizarItens();
        this.atualizarTotal();
        this.atualizarBotaoFinalizar();
    }

    renderizarItens() {
        const container = document.getElementById('carrinho-itens');
        if (!container) return;

        if (this.itens.length === 0) {
            container.innerHTML = `
                <div class="carrinho-vazio">
                    <div class="carrinho-vazio-icon">🛒</div>
                    <h5 style="color: #8B0000;">Seu carrinho está vazio</h5>
                    <p>Adicione algumas poções mágicas para começar!</p>
                    <a href="/cardapio/" class="magical-btn">
                        📜 Ver Cardápio
                    </a>
                </div>
            `;
            return;
        }

        container.innerHTML = this.itens.map(item => `
            <div class="col-md-6 mb-4">
                <div class="magical-card carrinho-item" data-item-id="${item.id}" data-personalizada="${item.personalizada || false}">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h6 style="color: #3C2415;">${item.bebida}</h6>
                            ${item.personalizada ? '<span class="badge-personalizada">✨ Personalizada</span>' : ''}
                        </div>
                        <button class="btn btn-sm btn-outline-danger" onclick="carrinho.removerItem(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    
                    ${item.ingredientes && item.ingredientes.length > 0 ? `
                        <div class="ingredientes-lista mb-2">
                            <small style="color: #8B0000; font-weight: bold;">Ingredientes Mágicos:</small>
                            <ul style="list-style: none; padding-left: 0; font-size: 0.85rem; color: #666; margin-top: 0.5rem;">
                                ${item.ingredientes.map(ing => `<li>• ${ing}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${item.descricao_completa ? `
                        <div class="descricao-completa mb-2">
                            <small style="color: #8B0000; font-weight: bold;">Fórmula Mágica:</small>
                            <p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">${item.descricao_completa}</p>
                        </div>
                    ` : ''}
                    
                    <div class="quantidade-controls">
                        <button class="quantidade-btn" onclick="carrinho.atualizarQuantidade(${item.id}, ${item.quantidade - 1})">-</button>
                        <span class="quantidade-display">${item.quantidade}</span>
                        <button class="quantidade-btn" onclick="carrinho.atualizarQuantidade(${item.id}, ${item.quantidade + 1})">+</button>
                    </div>
                    
                    <div class="mt-3">
                        <textarea class="form-control" placeholder="Observações especiais..." 
                                  onchange="carrinho.atualizarObservacoes(${item.id}, this.value)"
                                  style="font-size: 0.9rem;">${item.observacoes}</textarea>
                    </div>
                    
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <span class="item-preco">R$ ${(item.preco * item.quantidade).toFixed(2)}</span>
                        <small style="color: #666;">Unit: R$ ${item.preco.toFixed(2)}</small>
                    </div>
                </div>
            </div>
        `).join('');
    }

    atualizarTotal() {
        const totalElement = document.getElementById('carrinho-total');
        if (totalElement) {
            totalElement.textContent = `R$ ${this.calcularTotal().toFixed(2)}`;
        }
    }

    atualizarBotaoFinalizar() {
        const botao = document.getElementById('btn-finalizar');
        if (botao) {
            if (this.itens.length === 0) {
                botao.disabled = true;
                botao.textContent = 'Carrinho Vazio';
            } else {
                botao.disabled = false;
                botao.textContent = `💰 Finalizar Pedido (${this.itens.length} ${this.itens.length === 1 ? 'item' : 'itens'})`;
            }
        }
    }

    setupEventListeners() {
        // Event listener para finalizar pedido
        document.addEventListener('click', (e) => {
            if (e.target.id === 'btn-finalizar' && !e.target.disabled) {
                this.finalizarPedido();
            }
        });
    }

    finalizarPedido() {
        if (this.itens.length === 0) {
            showMagicalNotification('Adicione itens ao carrinho primeiro! 🛒', 'warning');
            return;
        }

        // Salvar pedido no sessionStorage para usar na página de pagamento
        sessionStorage.setItem('pedido_finalizar', JSON.stringify({
            itens: this.itens,
            total: this.calcularTotal(),
            timestamp: new Date().toISOString()
        }));

        showMagicalNotification('Redirecionando para pagamento... 💳', 'info');
        
        // Redirecionar para página de pagamento
        setTimeout(() => {
            window.location.href = '/pedido/pagamento/';
        }, 1000);
    }

    // Função para sincronizar com dados da sessão (se houver)
    sincronizarComSessao() {
        fetch('/pedido/api/sincronizar-carrinho/')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.itens_sessao) {
                // Mesclar itens da sessão com localStorage
                const itensExistentes = this.itens;
                const novasItems = data.itens_sessao.filter(itemSessao => {
                    return !itensExistentes.some(item => 
                        item.bebida === itemSessao.bebida_nome && 
                        item.timestamp === itemSessao.timestamp
                    );
                });

                if (novasItems.length > 0) {
                    // Converter formato da sessão para formato do carrinho
                    const itensConvertidos = novasItems.map(item => ({
                        id: Date.now() + Math.random(),
                        bebida: item.bebida_nome,
                        preco: item.preco_total,
                        quantidade: 1,
                        ingredientes: item.ingredientes || [],
                        observacoes: item.observacoes || '',
                        descricao_completa: item.descricao_completa || '',
                        personalizada: item.personalizada || false,
                        timestamp: item.timestamp
                    }));

                    this.itens.push(...itensConvertidos);
                    this.salvarCarrinho();
                    this.atualizarInterface();
                    
                    if (itensConvertidos.length > 0) {
                        showMagicalNotification(`${itensConvertidos.length} poção(ões) sincronizada(s) com seu carrinho!`, 'success');
                    }
                }
            }
        })
        .catch(error => {
            console.log('Sincronização opcional não disponível:', error);
        });
    }
}

// Classe para Rastreamento de Pedidos
class RastreamentoManager {
    constructor() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        const btnRastrear = document.getElementById('btn-rastrear');
        const inputCodigo = document.getElementById('codigo-rastreamento');

        if (btnRastrear) {
            btnRastrear.addEventListener('click', () => {
                const codigo = inputCodigo.value.trim();
                if (codigo) {
                    this.rastrearPedido(codigo);
                } else {
                    showMagicalNotification('Digite o código do pedido! 📝', 'warning');
                }
            });
        }

        if (inputCodigo) {
            inputCodigo.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    btnRastrear.click();
                }
            });
        }
    }

    async rastrearPedido(codigo) {
        const resultDiv = document.getElementById('tracking-result');
        if (!resultDiv) return;

        // Mostrar loading
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="text-center">
                <div class="spinner-border" role="status" style="color: #D4AF37;">
                    <span class="visually-hidden">Buscando...</span>
                </div>
                <p class="mt-2">Localizando sua poção mágica...</p>
            </div>
        `;

        try {
            const response = await fetch(`/pedido/api/rastrear/${codigo}/`);
            const data = await response.json();

            if (data.success) {
                this.exibirResultadoRastreamento(data.pedido);
                showMagicalNotification('Pedido encontrado! 🔍', 'success');
            } else {
                this.exibirErroRastreamento(data.message);
                showMagicalNotification(data.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao rastrear pedido:', error);
            this.exibirErroRastreamento('Erro ao conectar com o servidor');
            showMagicalNotification('Erro ao rastrear pedido!', 'error');
        }
    }

    exibirResultadoRastreamento(pedido) {
        const resultDiv = document.getElementById('tracking-result');
        
        const timeline = this.gerarTimeline(pedido.status, pedido.created_at);
        
        resultDiv.innerHTML = `
            <div class="text-center mb-4">
                <h5 style="color: #8B0000;">🔮 ${pedido.bebida}</h5>
                <p style="color: #666;">Pedido #${pedido.id} - Total: R$ ${pedido.preco}</p>
                <span class="status-badge status-${pedido.status.toLowerCase().replace(' ', '-')}">
                    ${pedido.status}
                </span>
            </div>
            
            <div class="tracking-timeline">
                ${timeline}
            </div>
        `;
    }

    exibirErroRastreamento(mensagem) {
        const resultDiv = document.getElementById('tracking-result');
        resultDiv.innerHTML = `
            <div class="text-center">
                <div style="font-size: 3rem;">😔</div>
                <h6 style="color: #8B0000;">Pedido não encontrado</h6>
                <p style="color: #666;">${mensagem}</p>
                <button class="magical-btn" onclick="document.getElementById('tracking-result').style.display='none'">
                    Tentar Novamente
                </button>
            </div>
        `;
    }

    gerarTimeline(status, createdAt) {
        const etapas = [
            { nome: 'Pedido Recebido', icon: '✓', descricao: 'Sua poção foi registrada em nosso grimório' },
            { nome: 'Em Preparo', icon: '🧙‍♂️', descricao: 'Nossos baristas estão preparando sua poção' },
            { nome: 'Pronto', icon: '🎉', descricao: 'Sua bebida está pronta para retirada' },
            { nome: 'Entregue', icon: '✨', descricao: 'Aproveite sua poção mágica!' }
        ];

        const statusIndex = this.getStatusIndex(status);
        
        return etapas.map((etapa, index) => {
            let classe = '';
            let tempo = '';
            
            if (index < statusIndex) {
                classe = 'completed';
                tempo = this.calcularTempo(createdAt, index);
            } else if (index === statusIndex) {
                classe = 'active';
                tempo = 'Agora';
            } else {
                tempo = 'Aguardando...';
            }

            return `
                <div class="timeline-item ${classe}">
                    <div class="timeline-marker">${etapa.icon}</div>
                    <div class="timeline-content">
                        <h6>${etapa.nome}</h6>
                        <p>${etapa.descricao}</p>
                        <small>${tempo}</small>
                    </div>
                </div>
            `;
        }).join('');
    }

    getStatusIndex(status) {
        const statusMap = {
            'Recebido': 0,
            'Em preparo': 1,
            'Pronto': 2,
            'Entregue': 3
        };
        return statusMap[status] || 0;
    }

    calcularTempo(createdAt, etapaIndex) {
        // Simular tempos baseados na criação do pedido
        const created = new Date(createdAt);
        const minutosAdicionar = etapaIndex * 5; // 5 minutos por etapa
        const tempoEtapa = new Date(created.getTime() + minutosAdicionar * 60000);
        
        return tempoEtapa.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
}

// Funções utilitárias globais
function showMagicalNotification(message, type = 'info') {
    // Função que deve existir globalmente para mostrar notificações
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} magical-notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 350px;
        animation: slideInRight 0.5s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 500);
    }, 3000);
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar managers
    window.carrinho = new CarrinhoManager();
    window.rastreamento = new RastreamentoManager();
    
    // Animações iniciais
    const cards = document.querySelectorAll('.magical-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
        
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
    });
});
