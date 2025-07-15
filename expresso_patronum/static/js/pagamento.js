document.addEventListener('DOMContentLoaded', function() {
    // Elementos principais
    var orderItemsList = document.getElementById('order-items-list');
    var subtotalSpan = document.getElementById('subtotal');
    var paymentRadios = document.querySelectorAll('input[name="payment_method"]');
    var paymentDetails = document.getElementById('payment-details');
    var finishBtn = document.getElementById('finish-order-btn');
    var discountLine = document.getElementById('discount-line');
    var discountLabel = document.getElementById('discount-label');
    var discountAmount = document.getElementById('discount-amount');
    var finalTotal = document.getElementById('final-total');
    var selectedMethod = document.getElementById('selected-method');
    var selectedMethodName = document.getElementById('selected-method-name');

    // Carrega itens do pedido do localStorage
    var carrinho = [];
    try {
        carrinho = JSON.parse(localStorage.getItem('carrinho_expresso')) || [];
    } catch (e) {
        carrinho = [];
    }

    // Renderiza os itens do pedido
    function renderOrderItems() {
        if (!carrinho.length) {
            orderItemsList.innerHTML = '<div style="color:#8B0000; text-align:center; font-size:1.1rem;">Nenhum item no caldeirão!</div>';
            subtotalSpan.innerHTML = '<strong>R$ 0,00</strong>';
            return 0;
        }
        var subtotal = 0;
        orderItemsList.innerHTML = '';
        carrinho.forEach(function(item, idx) {
            var ingredientesHtml = '';
            if (item.ingredientes && item.ingredientes.length) {
                ingredientesHtml = '<ul style="list-style: none; padding: 0; margin: 0; font-size: 0.9rem; color: #666;">' +
                    item.ingredientes.map(function(ing) { return '<li>• ' + ing + '</li>'; }).join('') + '</ul>';
            }
            var quantidade = item.quantidade ? parseInt(item.quantidade) : 1;
            var precoTotalItem = quantidade * parseFloat(item.preco);
            orderItemsList.innerHTML += 
                '<div class="order-item mb-3 p-3" style="border: 1px solid #D4AF37; border-radius: 10px; background: rgba(255,255,255,0.5);">' +
                '<div class="d-flex justify-content-between align-items-center">' +
                '<div>' +
                '<h6 style="color: #8B0000;">' + (item.bebida || 'Poção') + '</h6>' +
                ingredientesHtml +
                (item.observacoes ? "<div style='font-size:0.9rem;color:#3C2415;'>Obs: " + item.observacoes + "</div>" : '') +
                (quantidade > 1 ? "<div style='font-size:0.9rem;color:#666;'>Qtd: " + quantidade + "</div>" : '') +
                '</div>' +
                '<div class="text-end">' +
                '<div class="price" style="font-size: 1.2rem;">R$ ' + precoTotalItem.toFixed(2).replace('.', ',') + '</div>' +
                '<button class="btn btn-sm" style="color: #8B0000; font-size: 0.8rem;" onclick="removeItem(' + item.id + ')">🗑️ Remover</button>' +
                '</div>' +
                '</div>' +
                '</div>';
            subtotal += precoTotalItem;
        });
        subtotalSpan.innerHTML = '<strong>R$ ' + subtotal.toFixed(2).replace('.', ',') + '</strong>';
        var subtotalSummary = document.getElementById('subtotal-summary');
        if (subtotalSummary) {
            subtotalSummary.textContent = 'R$ ' + subtotal.toFixed(2).replace('.', ',');
        }
        return subtotal;
    }

    // Função para remover item do carrinho
    window.removeItem = function(itemId) {
        carrinho = carrinho.filter(function(item) { return item.id !== itemId; });
        localStorage.setItem('carrinho_expresso', JSON.stringify(carrinho));
        if (typeof showMagicalNotification === 'function') {
            showMagicalNotification('Item removido do caldeirão! 🗑️', 'info');
        }
        updatePricesAndPayment();
    };

    // Atualiza preços e descontos
    function updatePricesAndPayment() {
        var subtotal = renderOrderItems();
        var finalPrice = subtotal;
        var discount = 0;
        var methodName = '';
        
        paymentRadios.forEach(function(radio) {
            radio.onclick = function() {
                var method = this.value;
                finalPrice = subtotal;
                discount = 0;
                methodName = '';
                
                document.querySelectorAll('.payment-details').forEach(function(detail) {
                    detail.style.display = 'none';
                });
                
                switch(method) {
                    case 'fidelidade':
                        discount = subtotal * 0.10;
                        finalPrice = subtotal - discount;
                        methodName = '🎫 Cartão Fidelidade (-10%)';
                        document.getElementById('fidelidade-details').style.display = 'block';
                        break;
                    case 'pix':
                        discount = subtotal * 0.05;
                        finalPrice = subtotal - discount;
                        methodName = '💳 PIX Mágico (-5%)';
                        document.getElementById('pix-details').style.display = 'block';
                        break;
                    case 'cartao':
                        methodName = '💳 Cartão de Crédito/Débito';
                        document.getElementById('cartao-details').style.display = 'block';
                        discount = 0;
                        finalPrice = subtotal;
                        // Exibir desconto 0,00 e manter bloco visível
                        discountLine.style.display = 'flex';
                        discountLabel.textContent = 'Desconto:';
                        discountAmount.textContent = '- R$ 0,00';
                        break;
                }
                
                if (discount > 0) {
                    discountLine.style.display = 'flex';
                    discountLabel.textContent = 'Desconto:';
                    discountAmount.textContent = '- R$ ' + discount.toFixed(2).replace('.', ',');
                } else {
                    discountLine.style.display = 'none';
                }
                
                finalTotal.textContent = 'R$ ' + finalPrice.toFixed(2).replace('.', ',');
                selectedMethodName.textContent = methodName;
                selectedMethod.style.display = 'block';
                paymentDetails.style.display = 'block';
                finishBtn.disabled = subtotal === 0;
                
                finalTotal.style.transform = 'scale(1.1)';
                setTimeout(function() {
                    finalTotal.style.transform = 'scale(1)';
                }, 200);
            };
        });
        
        finalTotal.textContent = 'R$ ' + subtotal.toFixed(2).replace('.', ',');
        finishBtn.disabled = subtotal === 0;
    }

    finishBtn.onclick = function() {
        var selectedPayment = document.querySelector('input[name="payment_method"]:checked');
        if (selectedPayment && carrinho.length) {
            this.disabled = true;
            this.innerHTML = '⏳ Processando Magia...';
            
            // Simular processamento de pagamento
            setTimeout(function() {
                // Após pagamento bem-sucedido, processar histórico
                processarPagamentoBemSucedido(selectedPayment.value, carrinho);
                
                document.getElementById('paid-amount').textContent = finalTotal.textContent;
                
                if (typeof bootstrap !== 'undefined') {
                    var modal = new bootstrap.Modal(document.getElementById('confirmacao-pagamento'));
                    modal.show();
                }
                
                if (typeof showMagicalNotification === 'function') {
                    showMagicalNotification('Pagamento realizado com sucesso! 🎉', 'success');
                }
            }, 2000);
        }
    };

    // Função para processar pagamento bem-sucedido
    async function processarPagamentoBemSucedido(metodoPagamento, itensCarrinho) {
        try {
            // Salvar pedidos no banco de dados
            const response = await fetch('/pedidos/api/salvar-pedidos-localstorage/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    pedidos: itensCarrinho,
                    cliente: 'Cliente Anônimo',
                    metodo_pagamento: metodoPagamento
                })
            });

            const data = await response.json();

            if (data.success) {
                // Limpar carrinho local após salvar no banco
                localStorage.removeItem('carrinho_expresso');

                // Preencher modal com dados do pedido salvo
                if (data.pedidos && data.pedidos.length > 0) {
                    // Supondo que o backend retorna um array de pedidos
                    const pedido = data.pedidos[data.pedidos.length - 1];
                    document.getElementById('order-number').textContent = pedido.numero ? `#${pedido.numero}` : `#${pedido.id || '---'}`;
                    document.getElementById('paid-amount').textContent = pedido.total ? `R$ ${pedido.total.toFixed(2).replace('.', ',')}` : finalTotal.textContent;
                }

                // Configurar redirecionamento para rota correta após fechar modal
                setTimeout(function() {
                    window.location.href = '/cliente/historico/?pagamento=sucesso';
                }, 3000);

                if (typeof showMagicalNotification === 'function') {
                    showMagicalNotification(`${data.pedidos.length} pedido(s) salvo(s) no histórico! 📜`, 'success');
                }
            } else {
                console.error('Erro ao salvar pedidos:', data.message);
                if (typeof showMagicalNotification === 'function') {
                    showMagicalNotification('Erro ao salvar pedidos no histórico!', 'error');
                }
            }
        } catch (error) {
            console.error('Erro ao processar pagamento:', error);
            if (typeof showMagicalNotification === 'function') {
                showMagicalNotification('Erro ao processar pagamento!', 'error');
            }
        }
    }

    // Função para obter token CSRF
    function getCsrfToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            return csrfToken.value;
        }
        
        // Buscar no cookie se não estiver no DOM
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    // Formatação de cartão
    var cardNumberInput = document.querySelector('input[placeholder="0000 0000 0000 0000"]');
    if (cardNumberInput) {
        cardNumberInput.oninput = function() {
            var value = this.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            var formattedValue = value.match(/.{1,4}/g);
            this.value = formattedValue ? formattedValue.join(' ') : value;
        };
    }
    
    // Formatação de validade
    var validityInput = document.querySelector('input[placeholder="MM/AA"]');
    if (validityInput) {
        validityInput.oninput = function() {
            var value = this.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0,2) + '/' + value.substring(2,4);
            }
            this.value = value;
        };
    }

    // Inicializa renderização e preços
    updatePricesAndPayment();
});
