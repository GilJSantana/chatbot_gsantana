const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

describe('Chatbot Interface', () => {
  let document;
  let window;

  beforeEach(() => {
    const html = fs.readFileSync(path.resolve(__dirname, '../../html/index.html'), 'utf8');
    
    const dom = new JSDOM(html, {
      runScripts: 'dangerously',
      url: 'http://localhost'
    });

    window = dom.window;
    document = window.document;
    global.document = document; // Ainda útil para algumas APIs do Jest

    // CORREÇÃO: Anexa o mock do fetch diretamente na 'window' do JSDOM
    window.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ reply: 'Olá! Como posso ajudar?' }),
      })
    );

    // Mock do localStorage
    const localStorageMock = (function() {
      let store = {};
      return {
        getItem: function(key) { return store[key] || null; },
        setItem: function(key, value) { store[key] = value.toString(); },
        clear: function() { store = {}; },
        removeItem: function(key) { delete store[key]; }
      };
    })();
    
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock
    });

    // Carrega e executa o script principal
    const scriptContent = fs.readFileSync(path.resolve(__dirname, '../../html/script.js'), 'utf8');
    const scriptElement = document.createElement('script');
    scriptElement.textContent = scriptContent;
    document.body.appendChild(scriptElement);
  });

  test('should open chat window when chatbot icon is clicked', async () => {
    const chatbotIconContainer = document.getElementById('chatbotIconContainer');
    const chatbotWindow = document.getElementById('chatbotWindow');

    expect(chatbotWindow.classList.contains('open')).toBe(false);

    await window.Promise.resolve().then(() => {
      chatbotIconContainer.click();
    });

    expect(chatbotWindow.classList.contains('open')).toBe(true);
    expect(chatbotIconContainer.style.display).toBe('none');
  });

  test('should close chat window when close button is clicked', async () => {
    const chatbotIconContainer = document.getElementById('chatbotIconContainer');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const closeChatBtn = document.getElementById('closeChat');

    await window.Promise.resolve().then(() => {
      chatbotIconContainer.click();
    });
    expect(chatbotWindow.classList.contains('open')).toBe(true);

    closeChatBtn.click();

    expect(chatbotWindow.classList.contains('open')).toBe(false);
    expect(chatbotIconContainer.style.display).toBe('flex');
  });
});
