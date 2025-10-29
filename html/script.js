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

// --- Funções de Gerenciamento de Sessão e Estado ---

function getOrSetSessionId() {
    let sessionId = localStorage.getItem('chatbot_session_id');
    if (!sessionId) {
        sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
        localStorage.setItem('chatbot_session_id', sessionId);
    }
    return sessionId;
}

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

async function sendMessageToApi(message) {
    const sessionId = getOrSetSessionId();
    const typingIndicatorId = showTypingIndicator();

    try {
        const response = await fetch('/api/v1/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ session_id: sessionId, message: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const botResponse = data.reply; // CORREÇÃO: Usa "reply" em vez de "answer"

        removeTypingIndicator(typingIndicatorId);
        addMessage('bot', botResponse);

    } catch (error) {
        console.error('Erro ao contatar a API:', error);
        removeTypingIndicator(typingIndicatorId);
        addMessage('bot', 'Desculpe, estou com problemas para me conectar. Tente novamente mais tarde.');
    }
}

function handleUserMessage() {
    const message = chatInput.value.trim();
    if (message) {
        addMessage('user', message);
        chatInput.value = '';
        sendMessageToApi(message);
    }
}

// --- Funções de UI e Estado ---

async function openChatWindow() {
    chatbotWindow.classList.add('open');
    chatbotIconContainer.style.display = 'none';
    clearTimeout(welcomeBubbleTimeout);
    welcomeBubble.style.opacity = '0';
    welcomeBubble.style.visibility = 'hidden';

    // Se o chat estiver vazio, inicia a conversa com a FSM
    if (chatBody.children.length === 0) {
        await sendMessageToApi("Olá"); // Inicia o fluxo de onboarding
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

sendMessageBtn.addEventListener('click', handleUserMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleUserMessage();
    }
});

document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keypress', resetInactivityTimer);
document.addEventListener('scroll', resetInactivityTimer);

resetInactivityTimer();
