// JavaScript mágico para Expresso Patronum
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona efeitos mágicos aos elementos
    addMagicalEffects();
    
    // Inicializa animações
    initAnimations();
    
    // Configura interações dos ingredientes
    setupIngredientInteractions();
    
    // Configura sistema de notificações
    setupNotifications();
});

function addMagicalEffects() {
    // Adiciona partículas mágicas ao header
    const header = document.querySelector('.magical-header');
    if (header) {
        createMagicalParticles(header);
    }
    
    // Adiciona efeito hover aos cartões
    const cards = document.querySelectorAll('.magical-card, .beverage-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            createSparkles(this);
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            removeSparkles(this);
        });
    });
}

function createMagicalParticles(container) {
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'magical-particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #D4AF37;
            border-radius: 50%;
            pointer-events: none;
            animation: float ${2 + Math.random() * 3}s ease-in-out infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            opacity: ${0.3 + Math.random() * 0.7};
        `;
        container.appendChild(particle);
    }
}

function createSparkles(element) {
    const sparkleCount = 5;
    
    for (let i = 0; i < sparkleCount; i++) {
        const sparkle = document.createElement('div');
        sparkle.innerHTML = '✨';
        sparkle.className = 'sparkle-effect';
        sparkle.style.cssText = `
            position: absolute;
            pointer-events: none;
            font-size: 1rem;
            animation: sparkle ${1 + Math.random()}s ease-out forwards;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            z-index: 1000;
        `;
        element.appendChild(sparkle);
        
        setTimeout(() => sparkle.remove(), 1000);
    }
}

function removeSparkles(element) {
    const sparkles = element.querySelectorAll('.sparkle-effect');
    sparkles.forEach(sparkle => sparkle.remove());
}

function initAnimations() {
    // Animação de entrada para os elementos
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    document.querySelectorAll('.magical-card, .beverage-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function setupIngredientInteractions() {
    // Gerencia seleção de ingredientes na personalização
    const ingredientCheckboxes = document.querySelectorAll('input[name="ingredientes"]');
    const priceDisplay = document.querySelector('.total-price');
    
    if (ingredientCheckboxes.length > 0 && priceDisplay) {
        ingredientCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateTotalPrice);
        });
    }
}

function updateTotalPrice() {
    const basePrice = parseFloat(document.querySelector('#base-price').textContent || '0');
    const ingredientCheckboxes = document.querySelectorAll('input[name="ingredientes"]:checked');
    let totalIngredients = 0;
    
    ingredientCheckboxes.forEach(checkbox => {
        totalIngredients += parseFloat(checkbox.dataset.price || '0');
    });
    
    const total = basePrice + totalIngredients;
    const priceDisplay = document.querySelector('.total-price');
    if (priceDisplay) {
        priceDisplay.textContent = `R$ ${total.toFixed(2)}`;
        
        // Efeito mágico no preço
        priceDisplay.style.transform = 'scale(1.1)';
        setTimeout(() => {
            priceDisplay.style.transform = 'scale(1)';
        }, 200);
    }
}

function setupNotifications() {
    // Sistema de notificações em tempo real para pedidos
    if (window.location.pathname.includes('pedidos') || window.location.pathname.includes('cozinha')) {
        // Simula atualização de status (em produção seria WebSocket)
        setInterval(checkOrderUpdates, 10000); // Verifica a cada 10 segundos
    }
}

function checkOrderUpdates() {
    // Simula verificação de atualizações (em produção seria uma chamada AJAX)
    const statusElements = document.querySelectorAll('.status-badge');
    
    statusElements.forEach(element => {
        // Adiciona efeito de pulso quando há atualização
        element.style.animation = 'pulse 0.5s ease-in-out';
        setTimeout(() => {
            element.style.animation = '';
        }, 500);
    });
}

function showMagicalNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `magical-notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">✨</span>
            <span class="notification-message">${message}</span>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #D4AF37, #CD7F32);
        color: #3C2415;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        font-family: 'Crimson Text', serif;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    // Animação de entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove automaticamente após 5 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Função para ordenar bebida
function orderBeverage(beverageId, customizations = []) {
    showMagicalNotification('Sua poção está sendo preparada! 🧙‍♂️', 'success');
    
    // Aqui seria feita a chamada AJAX para o backend
    // Por enquanto, simula o processo
    setTimeout(() => {
        showMagicalNotification('Pedido enviado para a cozinha mágica!', 'info');
    }, 1000);
}

// Função para atualizar status do pedido
function updateOrderStatus(orderId, newStatus) {
    const statusElement = document.querySelector(`[data-order-id="${orderId}"] .status-badge`);
    if (statusElement) {
        statusElement.className = `status-badge status-${newStatus.toLowerCase().replace(' ', '-')}`;
        statusElement.textContent = newStatus;
        
        // Efeito mágico
        createSparkles(statusElement.parentElement);
        showMagicalNotification(`Seu pedido está ${newStatus}!`, 'info');
    }
}

// Adiciona CSS para animações extras
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .magical-notification {
        backdrop-filter: blur(10px);
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .notification-icon {
        font-size: 1.2rem;
    }
`;
document.head.appendChild(style);
