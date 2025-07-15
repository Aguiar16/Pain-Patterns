// Integração do Carrinho com Cardápio Principal
// Este arquivo demonstra como integrar poções do cardápio normal com o carrinho

// Função para adicionar bebida do cardápio ao carrinho
function adicionarBebidaCardapio(bebidaNome, preco, slug) {
    // Verificar se o carrinho existe
    if (window.carrinho) {
        window.carrinho.adicionarItem(bebidaNome, preco, []);
    } else {
        // Fallback para localStorage direto
        let carrinhoLocal = JSON.parse(localStorage.getItem('carrinho_expresso') || '[]');
        
        const novoItem = {
            id: Date.now(),
            bebida: bebidaNome,
            preco: parseFloat(preco),
            quantidade: 1,
            ingredientes: [],
            observacoes: '',
            personalizada: false,
            timestamp: new Date().toISOString()
        };
        
        carrinhoLocal.push(novoItem);
        localStorage.setItem('carrinho_expresso', JSON.stringify(carrinhoLocal));
        
        showMagicalNotification(`✨ ${bebidaNome} adicionado ao carrinho!`, 'success');
    }
}

// Função para redirecionar para personalização
function personalizarBebida(slug) {
    window.location.href = `/menu/personalizar/${slug}/`;
}

// Event listeners para botões do cardápio
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar botões de "Adicionar ao Carrinho" em cada card do cardápio
    const bebidaCards = document.querySelectorAll('.beverage-card, .magical-card');
    
    bebidaCards.forEach(card => {
        // Verificar se já tem botões
        if (card.querySelector('.btn-carrinho')) return;
        
        // Extrair informações da bebida
        const nome = card.querySelector('h3, h4, h5')?.textContent || 'Bebida';
        const precoElement = card.querySelector('.price, .preco');
        const preco = precoElement ? 
            parseFloat(precoElement.textContent.replace(/[^\d,]/g, '').replace(',', '.')) : 0;
        
        // Criar container de botões
        const botoesContainer = document.createElement('div');
        botoesContainer.className = 'carrinho-actions mt-3 text-center';
        botoesContainer.innerHTML = `
            <button class="magical-btn btn-carrinho" onclick="adicionarBebidaCardapio('${nome}', ${preco}, 'default')" 
                    style="margin-right: 0.5rem; font-size: 0.9rem; padding: 0.5rem 1rem;">
                🛒 Adicionar
            </button>
            <button class="magical-btn" onclick="personalizarBebida('default')" 
                    style="background: #D4AF37; font-size: 0.9rem; padding: 0.5rem 1rem;">
                ✨ Personalizar
            </button>
        `;
        
        // Adicionar ao card
        card.appendChild(botoesContainer);
    });
    
    // Atualizar contador do carrinho na navegação
    atualizarContadorCarrinho();
});

// Função para atualizar contador do carrinho
function atualizarContadorCarrinho() {
    const carrinho = JSON.parse(localStorage.getItem('carrinho_expresso') || '[]');
    const contador = document.querySelector('.carrinho-contador');
    
    if (contador) {
        const totalItens = carrinho.reduce((total, item) => total + item.quantidade, 0);
        contador.textContent = totalItens;
        contador.style.display = totalItens > 0 ? 'inline-block' : 'none';
    }
}

// Função global para remover do localStorage (para debug)
window.limparCarrinhoDebug = function() {
    localStorage.removeItem('carrinho_expresso');
    if (window.carrinho) {
        window.carrinho.itens = [];
        window.carrinho.atualizarInterface();
    }
    showMagicalNotification('Carrinho limpo para debug!', 'info');
};
