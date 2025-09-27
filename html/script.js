const chatbotIconContainer = document.getElementById('chatbotIconContainer');
const chatbotWindow = document.getElementById('chatbotWindow');
const closeChat = document.getElementById('closeChat');
const minimizeChat = document.getElementById('minimizeChat');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const sendMessageBtn = document.getElementById('sendMessage');
const welcomeBubble = document.getElementById('welcomeBubble');

let welcomeBubbleTimeout;
let inactivityTimer;

// --- Funções do Chat ---

function addMessage(sender, text, isHtml = false) {
    const messageId = `msg-${Date.now()}`;
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.id = messageId;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('message-bubble');

    if (isHtml) {
        bubbleDiv.innerHTML = text;
    } else {
        bubbleDiv.textContent = text;
    }

    messageDiv.appendChild(bubbleDiv);
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
    return messageId;
}

function showTypingIndicator() {
    return addMessage('bot', '<div class="typing-indicator"><span></span><span></span><span></span></div>', true);
}

function removeTypingIndicator(indicatorId) {
    const indicator = document.getElementById(indicatorId);
    if (indicator) {
        indicator.remove();
    }
}

async function handleUserMessage(message) {
    // 1. Adiciona a mensagem do usuário à interface
    addMessage('user', message);
    chatInput.value = '';

    // 2. Mostra o indicador de "digitando..."
    const typingIndicatorId = showTypingIndicator();

    try {
        // 3. Envia a pergunta para a API no endpoint correto com a barra final
        const response = await fetch('/api/v1/chat/', { // CORREÇÃO: Adicionada a barra final
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const botResponse = data.answer; // Assumindo que a API retorna { "answer": "..." }

        // 4. Remove o indicador e exibe a resposta da API
        removeTypingIndicator(typingIndicatorId);
        addMessage('bot', botResponse);

    } catch (error) {
        console.error('Erro ao contatar a API:', error);
        // 5. Remove o indicador e exibe uma mensagem de erro
        removeTypingIndicator(typingIndicatorId);
        addMessage('bot', 'Desculpe, estou com problemas para me conectar. Tente novamente mais tarde.');
    }
}

// --- Funções de UI e Estado ---

function openChatWindow() {
    chatbotWindow.classList.add('open');
    chatbotIconContainer.style.display = 'none';
    clearTimeout(welcomeBubbleTimeout);
    welcomeBubble.style.opacity = '0';
    welcomeBubble.style.visibility = 'hidden';

    if (chatBody.children.length === 0) {
        addMessage('bot', "Olá! Como posso ajudar você hoje?");
    }
}

function closeChatWindow() {
    chatbotWindow.classList.remove('open');
    chatbotIconContainer.style.display = 'flex';
    welcomeBubble.style.opacity = '';
    welcomeBubble.style.visibility = '';
    resetInactivityTimer();
}

function showWelcomeBubble() {
    if (!chatbotWindow.classList.contains('open')) {
        welcomeBubble.style.opacity = '1';
        welcomeBubble.style.visibility = 'visible';
        welcomeBubbleTimeout = setTimeout(() => {
            welcomeBubble.style.opacity = '0';
            welcomeBubble.style.visibility = 'hidden';
        }, 5000);
    }
}

function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    if (!chatbotWindow.classList.contains('open')) {
        inactivityTimer = setTimeout(showWelcomeBubble, 10000);
    }
}

// --- Event Listeners ---

chatbotIconContainer.addEventListener('click', openChatWindow);
closeChat.addEventListener('click', closeChatWindow);
minimizeChat.addEventListener('click', closeChatWindow);

sendMessageBtn.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (message) {
        handleUserMessage(message);
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessageBtn.click();
    }
});

document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keypress', resetInactivityTimer);
document.addEventListener('scroll', resetInactivityTimer);

resetInactivityTimer();
