# Command Pattern - Expresso Patronum

## 📋 Comandos Implementados

Este sistema implementa o **Command Pattern** completo para operações de pedidos, permitindo:

- ✅ **Executar comandos**
- ↩️ **Desfazer comandos (Undo)**
- ↪️ **Refazer comandos (Redo)**
- 📜 **Histórico de comandos**

---

## 🔧 Comandos Disponíveis

### 1. **FazerPedidoCommand** 🆕
Cria um novo pedido no sistema.

**Parâmetros:**
- `cliente`: Nome do cliente
- `bebida_personalizada`: Objeto BebidaPersonalizada (usando Decorator Pattern)
- `observacoes`: Instruções especiais (opcional)

**Exemplo:**
```python
comando = FazerPedidoCommand(
    cliente="Harry Potter",
    bebida_personalizada=bebida,
    observacoes="Extra quente, por favor!"
)
resultado = invoker.executar_comando(comando)
```

### 2. **CancelarPedidoCommand** ❌
Cancela um pedido existente.

**Parâmetros:**
- `pedido_id`: ID do pedido a ser cancelado
- `motivo`: Motivo do cancelamento (opcional)

**Restrições:**
- Não cancela pedidos já entregues
- Notifica observadores sobre o cancelamento

### 3. **AlterarPedidoCommand** ✏️
Altera um pedido existente.

**Parâmetros:**
- `pedido_id`: ID do pedido
- `nova_bebida_personalizada`: Nova bebida (opcional)
- `novo_cliente`: Novo nome do cliente (opcional)
- `novas_observacoes`: Novas instruções (opcional)

**Restrições:**
- Não altera pedidos em preparo, prontos ou entregues
- Apenas pedidos "Recebidos" podem ser alterados

---

## 🎮 Invoker - Gerenciador de Comandos

### **InvokerPedidos**
Classe responsável por:
- Executar comandos
- Manter histórico
- Implementar Undo/Redo
- Controlar sequência de comandos

**Métodos principais:**
```python
invoker = InvokerPedidos()

# Executar comando
resultado = invoker.executar_comando(comando)

# Desfazer último comando
resultado = invoker.desfazer()

# Refazer comando
resultado = invoker.refazer()

# Obter histórico
historico = invoker.obter_historico()
```

---

## 🌐 APIs Web Disponíveis

### **Fazer Pedido**
- **URL:** `POST /pedido/api/fazer-pedido/`
- **Dados:** Formulário com dados do carrinho
- **Uso:** Converte itens do carrinho em pedidos

### **Cancelar Pedido**
- **URL:** `POST /pedido/api/cancelar-pedido/<pedido_id>/`
- **Dados:** `motivo` (opcional)

### **Alterar Pedido**
- **URL:** `POST /pedido/api/alterar-pedido/<pedido_id>/`
- **Dados:** `novo_cliente`, `novas_observacoes`

### **Desfazer Comando**
- **URL:** `POST /pedido/api/desfazer/`
- **Retorna:** Resultado da operação de undo

### **Refazer Comando**
- **URL:** `POST /pedido/api/refazer/`
- **Retorna:** Resultado da operação de redo

### **Histórico**
- **URL:** `GET /pedido/api/historico/`
- **Retorna:** Lista completa de comandos executados

---

## 🖥️ Interface Web

### **Botões na Página de Pedidos:**
- **✏️ Alterar:** Abre modal para alterar pedido
- **❌ Cancelar:** Abre modal para cancelar pedido
- **📜 Ver Histórico:** Mostra histórico de comandos

### **Modais Disponíveis:**
1. **Modal de Alteração:** Permite alterar nome e observações
2. **Modal de Cancelamento:** Permite cancelar com motivo
3. **Modal de Histórico:** Mostra comandos e botões Undo/Redo

---

## 🧪 Demonstração

### **Management Command:**
```bash
python manage.py demo_commands
```

### **Script de Exemplo:**
```python
python exemplo_commands.py
```

### **Cenários Demonstrados:**
1. 🆕 Criar pedido para Harry Potter
2. ✏️ Alterar dados do pedido
3. ↩️ Desfazer alteração
4. ↪️ Refazer alteração
5. ❌ Cancelar pedido
6. 📊 Mostrar histórico completo

---

## 🏗️ Arquitetura

### **Padrões Integrados:**
- **Command Pattern:** Para operações de pedido
- **Observer Pattern:** Notificação de mudanças
- **State Pattern:** Estados do pedido
- **Decorator Pattern:** Personalização de bebidas
- **Strategy Pattern:** Políticas de desconto
- **DAO Pattern:** Acesso a dados
- **Business Object:** Lógica de negócio

### **Fluxo de Execução:**
```
Interface Web → API Controller → Command → Business Object → DAO → Database
                    ↓
               Invoker (histórico)
                    ↓
            Observer (notificações)
```

---

## ⚡ Benefícios Implementados

### **1. Desacoplamento**
- Comandos são independentes da interface
- Fácil adição de novos comandos
- Testabilidade isolada

### **2. Funcionalidades Avançadas**
- **Undo/Redo** completo
- **Histórico persistente** de operações
- **Validações** antes da execução

### **3. Experiência do Usuário**
- **Recuperação de erros** via Undo
- **Transparência** das operações
- **Feedback visual** em tempo real

### **4. Manutenibilidade**
- **Código organizado** por responsabilidade
- **Extensibilidade** para novos comandos
- **Logging automático** de operações

---

## 🎯 Casos de Uso Reais

### **Cenário 1: Cliente Indeciso**
1. Cliente faz pedido
2. Muda de ideia e altera
3. Muda novamente e desfaz
4. Confirma pedido final

### **Cenário 2: Problema Operacional**
1. Pedido é feito
2. Problema na cozinha - cancelamento
3. Problema resolvido - desfazer cancelamento
4. Pedido volta à produção

### **Cenário 3: Gerência**
1. Visualizar histórico de operações
2. Identificar padrões de cancelamento
3. Reverter operações incorretas
4. Auditoria de mudanças

---

## 🚀 Como Usar

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Executar Migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **3. Testar Comandos**
```bash
python manage.py demo_commands
```

### **4. Acessar Interface**
```
http://localhost:8000/pedido/
```

---

## 📝 Notas Técnicas

- **Thread Safety:** Invoker é thread-safe para múltiplos usuários
- **Persistência:** Histórico mantido em memória (pode ser persistido)
- **Performance:** Comandos otimizados para execução rápida
- **Observadores:** Integração automática com notificações

---

## 🎭 Tema Harry Potter

Toda a implementação mantém o tema mágico:
- **"Poções"** em vez de bebidas
- **"Bruxos/Bruxas"** em vez de clientes
- **"Comandos Mágicos"** em vez de comandos
- **"Caldeirão"** em vez de carrinho
- **Emojis temáticos:** ⚡🧙‍♂️🔮✨

**"A magia acontece quando você pode desfazer o que não deu certo!"** 🪄
