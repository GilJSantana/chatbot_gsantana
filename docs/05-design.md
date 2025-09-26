# 🎨 Processo de Design (UX/UI) do Chatbot Gsantana

Este documento descreve o processo de design da interface do Chatbot Gsantana, abordando as decisões de UX (Experiência do Usuário) e UI (Interface do Usuário). O objetivo foi criar uma experiência de chat simples, intuitiva e que se integre de forma harmoniosa com o site.

## 1. Pesquisa e Definição do Problema

O problema a ser resolvido era a necessidade de fornecer aos usuários do site um canal rápido e automatizado para obter respostas a perguntas frequentes. O design da solução se baseou em:

* **Identificação do Público:** Visitantes do site com perguntas específicas sobre testes, serviços ou o projeto em geral. Eles precisam de respostas rápidas sem a necessidade de procurar por páginas ou entrar em contato com o suporte.
* **Contexto de Uso:** A interface do chatbot precisa ser acessível em qualquer página do site e funcionar bem em dispositivos móveis e desktops.
* **Problema a Ser Resolvido:** Reduzir o tempo de espera do usuário por informações e desafogar a equipe de suporte.

## 2. Decisões de User Experience (UX)

A experiência do usuário foi projetada para ser o mais fluida possível, com foco nos seguintes pontos:

* **Interação Natural:** A interface de chat é um modelo de interação familiar para a maioria dos usuários, minimizando a curva de aprendizado.
* **Feedback Visual:** O chatbot deve fornecer feedback imediato ao usuário, como mensagens de "digitando..." ou ícones de carregamento, para indicar que a requisição está sendo processada.
* **Simplicidade:** O fluxo de interação é direto: o usuário pergunta, o chatbot responde. Não há menus complexos ou opções de navegação. A interface principal contém apenas o campo de entrada de texto e a área de exibição das mensagens.
* **Design Não Intrusivo:** O chatbot é projetado como um componente que não interfere na navegação normal do site. Ele pode ser minimizado ou fechado quando não estiver em uso.

## 3. Decisões de User Interface (UI)

O design visual da interface do chatbot foi pensado para ser limpo e funcional.

* **Paleta de Cores:** As cores foram escolhidas para harmonizar com a identidade visual do site do projeto (assumindo cores corporativas como azul e branco). Isso garante que o chatbot pareça uma parte nativa do site, e não um elemento externo.
* **Tipografia:** Foi utilizada uma fonte legível e moderna para as mensagens de texto, garantindo que o conteúdo seja fácil de ler tanto para o usuário quanto para o chatbot.
* **Componentes Visuais:**
    * **Ícone Flutuante:** Um ícone de balão de fala ou um avatar simples para representar o chatbot na tela, chamando a atenção do usuário para a funcionalidade.
    * **Caixa de Chat:** O chat é exibido em uma caixa retangular com bordas arredondadas, para uma sensação mais amigável.
    * **Mensagens:** As mensagens do usuário e do chatbot são diferenciadas por cores de fundo e alinhamento (ex: mensagens do usuário à direita com fundo azul, mensagens do chatbot à esquerda com fundo cinza claro).
    * **Campo de Entrada:** Um campo de texto simples, com um placeholder indicando "Digite sua pergunta...".
    * **Ícones:** Ícones claros e intuitivos para ações como enviar mensagem, fechar a janela ou minimizar o chat.

## 4. Protótipos e Mockups

## 💡 Mockup 1: Estado Inicial - Ícone Flutuante

Descrição: Um ícone de chat flutuante, posicionado fixamente no canto inferior direito da tela, visível em todas as páginas do site.

### Estilo

| Propriedade | Valor/Descrição |
| :--- | :--- |
| **Formato** | Círculo ou um "balão de fala" moderno e arredondado. |
| **Tamanho** | Aproximadamente $\mathbf{56px} \times \mathbf{56px}$. |
| **Cor de Fundo** | **Azul primário** do lab-yes.com (ex: `#007bff` ou um tom similar ao do logo). |
| **Cor do Ícone** | **Branco** (`#FFFFFF`). |
| **Ícone** | Um ícone de balão de fala ou um ícone de "chat" (ex: um ícone de mensagem com três pontos dentro). |
| **Sombra** | Uma sombra sutil para dar profundidade e destacá-lo (ex: `box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);`). |
| **Posicionamento** | `position: fixed; bottom: 20px; right: 20px; z-index: 1000;`. |
| **Transição** | Suave ao passar o mouse (ex: `transition: all 0.3s ease;`). |

### Interação

* **Hover**: Ao passar o cursor, leve animação de escala ou mudança de cor de fundo.
* **Caixa de Boas-Vindas (Opcional/Temporizada)**: Após 10-15 segundos, uma pequena caixa de diálogo retangular com bordas arredondadas surge acima do ícone.
    * **Conteúdo**: "Olá! Precisa de ajuda?" ou "Fale conosco!".
    * **Estilo**: Fundo branco, texto em cinza escuro (`#333`), seta apontando para o ícone. Desaparece após alguns segundos ou ao mover o mouse.

---

## 💬 Mockup 2: Chat Aberto - Caixa de Diálogo Principal

Descrição: Uma caixa de chat retangular que se expande a partir do ícone flutuante, ocupando uma área maior no canto inferior direito da tela.

### Estilo Geral

| Propriedade | Valor/Descrição |
| :--- | :--- |
| **Dimensões** | Largura de $\mathbf{350px}$ a $\mathbf{400px}$, altura de $\mathbf{450px}$ a $\mathbf{550px}$. |
| **Bordas** | Arredondadas (ex: `border-radius: 10px;`). |
| **Sombra** | Mais proeminente (ex: `box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);`). |
| **Fundo** | **Branco** (`#FFFFFF`). |
| **Posicionamento** | `position: fixed; bottom: 20px; right: 20px; z-index: 1001;`. |
| **Transição** | Animação suave de expansão ao abrir. |
| **Tipografia** | Fonte Arial, Helvetica, sans-serif (ou a fonte principal do lab-yes.com). |

### Cabeçalho

| Elemento | Estilo/Detalhes |
| :--- | :--- |
| **Altura** | Aproximadamente $\mathbf{50px}$. |
| **Cor de Fundo** | **Azul primário** do lab-yes.com (ex: `#007bff`). |
| **Texto** | "Chatbot Gsantana" ou "**Assistente Virtual**" em branco (`#FFFFFF`), `font-weight: bold; font-size: 1.1em;`. |
| **Ícones de Ação** | "Minimizar" e "**Fechar** ('X')" em branco, alinhados à direita. |
| **Avatar (Opcional)** | Pequeno avatar circular do chatbot à esquerda do título. |

### Área de Mensagens (`chat-body`)

| Elemento | Estilo/Detalhes |
| :--- | :--- |
| **Fundo** | Branco (`#FFFFFF`) ou cinza muito claro (`#F8F8F8`). |
| **Scroll** | `overflow-y: auto;` para permitir rolagem. |

#### Mensagens do Chatbot (Esquerda)

* **Balão**: Fundo cinza claro (ex: `#E0E0E0`), `border-radius: 15px 15px 15px 0;`.
* **Texto**: Cinza escuro (`#333`), `font-size: 0.95em;`.
* **Padding**: `10px 15px;`.

#### Mensagens do Usuário (Direita)

* **Balão**: Fundo **azul primário** (ex: `#007bff`), `border-radius: 15px 15px 0 15px;`.
* **Texto**: **Branco** (`#FFFFFF`), `font-size: 0.95em;`.
* **Padding**: `10px 15px;`.

### Área de Entrada (`chat-input`)

| Elemento | Estilo/Detalhes |
| :--- | :--- |
| **Campo de Texto** | `input type="text"` com `placeholder="Digite sua pergunta..."`. Borda sutil, `border-radius: 20px;`, `padding: 10px 15px;`. |
| **Botão de Enviar** | Ícone de avião de papel ou seta para a direita. Fundo **azul primário**, ícone branco, `border-radius: 50%;`, $\mathbf{40px} \times \mathbf{40px}$. |
| **Botões de Sugestões** | Botões retangulares com bordas arredondadas, fundo azul claro (ex: `#E6F2FF`) ou branco com borda azul, texto azul escuro. `padding: 8px 12px; margin: 5px;`.

---

## 🤝 Mockup 3: Exemplo de Interação

Descrição: Demonstração de um fluxo de conversa dentro da caixa de chat aberta.

### Fluxo Detalhado

1.  **Chatbot (Mensagem de Boas-Vindas):**
    > "Olá! Como posso ajudar você hoje?"
    > **Abaixo, botões de sugestão:** [Quais serviços vocês oferecem?], [Como entro em contato?], [Sobre o projeto Gsantana]

2.  **Usuário (Ação):** Clica no botão "**Quais serviços vocês oferecem?**"

3.  **Chatbot (Resposta):**
    > "Oferecemos testes de software, consultoria em QA e automação de testes. Gostaria de saber mais sobre algum deles?"
    > **Abaixo, botões de sugestão:** [Testes de Software], [Consultoria em QA], [Automação de Testes]

4.  **Usuário (Texto):** Digita "**Fale sobre automação de testes.**" e envia.

5.  **Chatbot (Resposta Detalhada):**
    > "A automação de testes visa otimizar o processo de validação de software, executando testes repetitivos de forma automática, o que aumenta a velocidade e a confiabilidade dos ciclos de desenvolvimento. Saiba mais **aqui**."
    > (Pode incluir um link formatado para uma página relevante no site lab-yes.com.)

    
## 5. Conclusão

O design do Chatbot Gsantana priorizou a **simplicidade e a funcionalidade**. A interface foi construída para ser um complemento útil e não intrusivo para a experiência do usuário no site, garantindo que o foco principal esteja na rápida obtenção de informações. A integração visual com o site [lab-yes.com](https://www.lab-yes.com) é fundamental para uma experiência coesa e profissional.

---

### Protótipo Funcional (HTML/CSS/JS)

Abaixo é apresentado o código-fonte completo do protótipo funcional do chatbot, demonstrando a integração visual e interativa discutida nos mockups.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Gsantana Prototype</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Variáveis de Cores (baseadas em lab-yes.com) */
        :root {
            --primary-blue: #007bff; /* Azul principal */
            --light-blue: #e6f2ff;   /* Azul claro para botões de sugestão */
            --text-dark: #333;       /* Texto escuro */
            --text-light: #fff;      /* Texto claro */
            --chat-bubble-bot: #e0e0e0; /* Balão do bot */
            --chat-background: #f8f8f8; /* Fundo da área de mensagens */
            --shadow-light: rgba(0, 0, 0, 0.2);
            --shadow-medium: rgba(0, 0, 0, 0.3);
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            min-height: 150vh; /* Para simular scroll e o ícone fixo */
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding-top: 50px;
        }

        .content {
            width: 80%;
            max-width: 900px;
            background-color: var(--text-light);
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px var(--shadow-light);
            text-align: center;
        }

        /* Ícone Flutuante */
        .chatbot-icon-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .chatbot-icon {
            width: 56px;
            height: 56px;
            background-color: var(--primary-blue);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0px 4px 8px var(--shadow-light);
            color: var(--text-light);
            font-size: 1.5em;
        }

        .chatbot-icon-container:hover {
            transform: translateY(-3px);
            box-shadow: 0px 6px 12px var(--shadow-medium);
        }

        /* Caixa de Boas-Vindas (Opcional) */
        .welcome-bubble {
            position: absolute;
            bottom: 70px; /* Acima do ícone */
            right: 0;
            background-color: var(--text-light);
            color: var(--text-dark);
            padding: 10px 15px;
            border-radius: 8px;
            box-shadow: 0px 2px 5px var(--shadow-light);
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
            font-size: 0.9em;
        }

        .welcome-bubble::after {
            content: '';
            position: absolute;
            bottom: -10px;
            right: 15px;
            border-width: 10px 10px 0;
            border-style: solid;
            border-color: var(--text-light) transparent transparent transparent;
        }

        .chatbot-icon-container:hover .welcome-bubble {
            opacity: 1;
            visibility: visible;
        }

        /* Chat Aberto */
        .chatbot-window {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 380px; /* Largura ajustada */
            height: 500px; /* Altura ajustada */
            background-color: var(--text-light);
            border-radius: 10px;
            box-shadow: 0px 8px 16px var(--shadow-medium);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            z-index: 1001;
            transform: scale(0); /* Escondido inicialmente */
            transform-origin: bottom right;
            transition: transform 0.3s ease-in-out;
        }

        .chatbot-window.open {
            transform: scale(1);
        }

        .chatbot-header {
            background-color: var(--primary-blue);
            color: var(--text-light);
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            font-size: 1.1em;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }

        .chatbot-header .actions i {
            margin-left: 15px;
            cursor: pointer;
        }

        .chatbot-body {
            flex-grow: 1;
            padding: 15px;
            overflow-y: auto;
            background-color: var(--chat-background);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .message {
            display: flex;
            max-width: 80%;
        }

        .message.bot {
            justify-content: flex-start;
        }

        .message.user {
            justify-content: flex-end;
            margin-left: auto; /* Empurra para a direita */
        }

        .message-bubble {
            padding: 10px 15px;
            border-radius: 15px;
            line-height: 1.4;
            word-wrap: break-word;
        }

        .message.bot .message-bubble {
            background-color: var(--chat-bubble-bot);
            color: var(--text-dark);
            border-bottom-left-radius: 0;
        }

        .message.user .message-bubble {
            background-color: var(--primary-blue);
            color: var(--text-light);
            border-bottom-right-radius: 0;
        }

        .suggestion-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
            justify-content: flex-start; /* Alinha botões à esquerda */
        }

        .suggestion-button {
            background-color: var(--light-blue);
            color: var(--primary-blue);
            border: 1px solid var(--primary-blue);
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background-color 0.2s ease, color 0.2s ease;
        }

        .suggestion-button:hover {
            background-color: var(--primary-blue);
            color: var(--text-light);
        }

        .chatbot-input-area {
            padding: 15px;
            border-top: 1px solid #eee;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .chatbot-input-area input {
            flex-grow: 1;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 20px;
            font-size: 1em;
            outline: none;
        }

        .chatbot-input-area button {
            background-color: var(--primary-blue);
            color: var(--text-light);
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.2em;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }

        .chatbot-input-area button:hover {
            background-color: #0056b3; /* Tom mais escuro do azul */
        }

        /* Link dentro da mensagem */
        .message-bubble a {
            color: var(--primary-blue);
            text-decoration: underline;
        }
        .message.user .message-bubble a {
            color: var(--text-light);
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Bem-vindo ao Site Lab-Yes!</h1>
        <p>Este é um conteúdo de exemplo para simular a presença do chatbot em uma página.</p>
        <p>Role para baixo para ver o ícone do chatbot fixo no canto inferior direito.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    </div>

    <!-- Ícone Flutuante do Chatbot -->
    <div class="chatbot-icon-container" id="chatbotIconContainer">
        <div class="chatbot-icon">
            <i class="fas fa-comment-dots"></i>
        </div>
        <div class="welcome-bubble" id="welcomeBubble">Olá! Precisa de ajuda?</div>
    </div>

    <!-- Janela do Chatbot -->
    <div class="chatbot-window" id="chatbotWindow">
        <div class="chatbot-header">
            <span>Chatbot Gsantana</span>
            <div class="actions">
                <i class="fas fa-minus" id="minimizeChat"></i>
                <i class="fas fa-times" id="closeChat"></i>
            </div>
        </div>
        <div class="chatbot-body" id="chatBody">
            <!-- Mensagens serão adicionadas aqui via JS -->
        </div>
        <div class="chatbot-input-area">
            <input type="text" id="chatInput" placeholder="Digite sua pergunta...">
            <button id="sendMessage">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>

    <script>
        const chatbotIconContainer = document.getElementById('chatbotIconContainer');
        const chatbotWindow = document.getElementById('chatbotWindow');
        const closeChat = document.getElementById('closeChat');
        const minimizeChat = document.getElementById('minimizeChat');
        const chatBody = document.getElementById('chatBody');
        const chatInput = document.getElementById('chatInput');
        const sendMessageBtn = document.getElementById('sendMessage');
        const welcomeBubble = document.getElementById('welcomeBubble');

        let welcomeBubbleTimeout;

        // Função para adicionar mensagem ao chat
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

        // Função para adicionar botões de sugestão
        function addSuggestionButtons(buttons) {
            const buttonsDiv = document.createElement('div');
            buttonsDiv.classList.add('message', 'bot'); // Para alinhar como mensagem do bot
            const bubbleDiv = document.createElement('div');
            bubbleDiv.classList.add('message-bubble'); // Para o estilo de balão
            const suggestionContainer = document.createElement('div');
            suggestionContainer.classList.add('suggestion-buttons');

            buttons.forEach(buttonText => {
                const button = document.createElement('button');
                button.classList.add('suggestion-button');
                button.textContent = buttonText;
                button.onclick = () => handleUserMessage(buttonText, true); // Simula clique no botão
                suggestionContainer.appendChild(button);
            });
            bubbleDiv.appendChild(suggestionContainer);
            buttonsDiv.appendChild(bubbleDiv);
            chatBody.appendChild(buttonsDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
        }

        // Lógica de interação do chatbot
        function handleUserMessage(message, isButtonClick = false) {
            if (!isButtonClick) {
                addMessage('user', message);
            }
            chatInput.value = ''; // Limpa o input

            // Simula resposta do bot
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
                    botResponse = "A automação de testes visa otimizar o processo de validação de software, executando testes repetitivos de forma automática, o que aumenta a velocidade e a confiabilidade dos ciclos de desenvolvimento. <a href='https://www.lab-yes.com/automacao-testes' target='_blank'>Saiba mais aqui</a>.";
                    addMessage('bot', botResponse, true); // Passa true para HTML
                    return; // Não adiciona resposta padrão nem botões depois de um link
                } else if (message.toLowerCase().includes('contato')) {
                    botResponse = "Você pode entrar em contato conosco através do nosso formulário no site ou pelo e-mail <a href='mailto:contato@lab-yes.com'>contato@lab-yes.com</a>.";
                    addMessage('bot', botResponse, true);
                    return;
                } else if (message.toLowerCase().includes('projeto gsantana')) {
                    botResponse = "O projeto Gsantana é um chatbot desenvolvido para auxiliar os usuários do site Lab-Yes com informações rápidas e eficientes.";
                }

                addMessage('bot', botResponse);
                if (suggestionButtons.length > 0) {
                    addSuggestionButtons(suggestionButtons);
                }
            }, 800);
        }

        // Eventos
        chatbotIconContainer.addEventListener('click', () => {
            chatbotWindow.classList.add('open');
            chatbotIconContainer.style.display = 'none'; // Esconde o ícone quando o chat abre
            clearTimeout(welcomeBubbleTimeout); // Limpa qualquer timeout da bolha de boas-vindas
            welcomeBubble.style.opacity = '0';
            welcomeBubble.style.visibility = 'hidden';

            // Mensagem inicial do bot
            if (chatBody.children.length === 0) {
                addMessage('bot', "Olá! Como posso ajudar você hoje?");
                addSuggestionButtons(["Quais serviços vocês oferecem?", "Como entro em contato?", "Sobre o projeto Gsantana"]);
            }
        });

        closeChat.addEventListener('click', () => {
            chatbotWindow.classList.remove('open');
            chatbotIconContainer.style.display = 'flex'; // Mostra o ícone novamente
        });

        minimizeChat.addEventListener('click', () => {
            chatbotWindow.classList.remove('open');
            chatbotIconContainer.style.display = 'flex'; // Mostra o ícone novamente
        });

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

        // Lógica da bolha de boas-vindas temporizada
        function showWelcomeBubble() {
            if (!chatbotWindow.classList.contains('open')) {
                welcomeBubble.style.opacity = '1';
                welcomeBubble.style.visibility = 'visible';
                welcomeBubbleTimeout = setTimeout(() => {
                    welcomeBubble.style.opacity = '0';
                    welcomeBubble.style.visibility = 'hidden';
                }, 5000); // Desaparece após 5 segundos
            }
        }

        // Mostra a bolha de boas-vindas após um tempo de inatividade
        let inactivityTimer;
        function resetInactivityTimer() {
            clearTimeout(inactivityTimer);
            if (!chatbotWindow.classList.contains('open')) {
                inactivityTimer = setTimeout(showWelcomeBubble, 10000); // 10 segundos de inatividade
            }
        }

        document.addEventListener('mousemove', resetInactivityTimer);
        document.addEventListener('keypress', resetInactivityTimer);
        document.addEventListener('scroll', resetInactivityTimer);
        resetInactivityTimer(); // Inicia o timer ao carregar a página
    </script>
</body>
</html>