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
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('message-bubble');
    if (isHtml) {
        bubbleDiv.innerHTML = text;
    } else {
        bubbleDiv.textContent = text;
    }
    messageDiv.appendChild(bubbleDiv);
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight; // Rola para o final
}

function addSuggestionButtons(buttons) {
    const buttonsDiv = document.createElement('div');
    buttonsDiv.classList.add('message', 'bot');
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('message-bubble');
    const suggestionContainer = document.createElement('div');
    suggestionContainer.classList.add('suggestion-buttons');

    buttons.forEach(buttonText => {
        const button = document.createElement('button');
        button.classList.add('suggestion-button');
        button.textContent = buttonText;
        button.onclick = () => handleUserMessage(buttonText, true);
        suggestionContainer.appendChild(button);
    });
    bubbleDiv.appendChild(suggestionContainer);
    buttonsDiv.appendChild(bubbleDiv);
    chatBody.appendChild(buttonsDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function handleUserMessage(message, isButtonClick = false) {
    if (!isButtonClick) {
        addMessage('user', message);
    }
    chatInput.value = '';

    setTimeout(() => {
        let botResponse = "Desculpe, não entendi sua pergunta. Posso ajudar com outra coisa?";
        let suggestionButtons = [];

        if (message.toLowerCase().includes('olá') || message.toLowerCase().includes('oi') || message.toLowerCase().includes('ajuda')) {
            botResponse = "Olá! Como posso ajudar você hoje?";
            suggestionButtons = ["Quais serviços vocês oferecem?", "Como entro em contato?", "Sobre o projeto Gsantana"];
        } else if (message.toLowerCase().includes('serviços')) {
            botResponse = "Oferecemos testes de software, consultoria em QA e automação de testes. Gostaria de saber mais sobre algum deles?";
            suggestionButtons = ["Testes de Software", "Consultoria em QA", "Automação de Testes"];
        } else if (message.toLowerCase().includes('automação de testes')) {
            botResponse = "A automação de testes visa otimizar o processo de validação de software... <a href='https://www.lab-yes.com/automacao-testes' target='_blank'>Saiba mais aqui</a>.";
            addMessage('bot', botResponse, true);
            return;
        } else if (message.toLowerCase().includes('contato')) {
            botResponse = "Você pode nos contatar em <a href='mailto:contato@lab-yes.com'>contato@lab-yes.com</a>.";
            addMessage('bot', botResponse, true);
            return;
        } else if (message.toLowerCase().includes('projeto gsantana')) {
            botResponse = "O projeto Gsantana é um chatbot para auxiliar os usuários do site Lab-Yes.";
        }

        addMessage('bot', botResponse);
        if (suggestionButtons.length > 0) {
            addSuggestionButtons(suggestionButtons);
        }
    }, 800);
}

// --- Funções de UI e Estado ---

function openChatWindow() {
    chatbotWindow.classList.add('open');
    chatbotIconContainer.style.display = 'none';
    clearTimeout(welcomeBubbleTimeout);
    // Adiciona estilos inline para esconder a bolha ao abrir o chat
    welcomeBubble.style.opacity = '0';
    welcomeBubble.style.visibility = 'hidden';

    if (chatBody.children.length === 0) {
        addMessage('bot', "Olá! Como posso ajudar você hoje?");
        addSuggestionButtons(["Quais serviços vocês oferecem?", "Como entro em contato?", "Sobre o projeto Gsantana"]);
    }
}

function closeChatWindow() {
    chatbotWindow.classList.remove('open');
    chatbotIconContainer.style.display = 'flex';
    // BUG FIX: Remove os estilos inline para que o CSS :hover volte a funcionar
    welcomeBubble.style.opacity = '';
    welcomeBubble.style.visibility = '';
    resetInactivityTimer(); // Reinicia o timer para a bolha poder aparecer novamente
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

// Inicia o ciclo de vida do chatbot
resetInactivityTimer();
