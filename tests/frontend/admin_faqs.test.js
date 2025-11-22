const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const mockFaqs = [
    { id: 1, question: 'Q1', answer: 'A1' },
    { id: 2, question: 'Q2', answer: 'A2' },
];

describe('Admin FAQs Management Interface', () => {
    let document;
    let window;

    beforeEach(() => {
        const html = fs.readFileSync(path.resolve(__dirname, '../../html/admin/faqs.html'), 'utf8');
        const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost/admin/faqs.html' });
        
        window = dom.window;
        document = window.document;

        // CORREÇÃO: Configura todos os mocks ANTES de carregar o script
        
        // Mock do localStorage (usuário logado)
        Object.defineProperty(window, 'localStorage', {
            value: (function() {
                let store = { 'access_token': 'fake_token' };
                return {
                    getItem: function(key) { return store[key] || null; },
                    setItem: function(key, value) { store[key] = value.toString(); },
                    removeItem: function(key) { delete store[key]; },
                };
            })()
        });

        // Mocks do navegador
        window.fetch = jest.fn();
        window.alert = jest.fn();
        window.confirm = jest.fn(() => true);
        Object.defineProperty(window, 'location', {
            writable: true,
            value: { href: 'http://localhost/admin/faqs.html' }
        });

        // Configura o mock do fetch para a chamada inicial que acontece no carregamento do script
        window.fetch.mockResolvedValue({
            ok: true,
            json: async () => mockFaqs,
        });

        // Carrega o script DEPOIS que todos os mocks estão prontos
        const scriptContent = fs.readFileSync(path.resolve(__dirname, '../../html/admin/js/faqs.js'), 'utf8');
        const scriptElement = document.createElement('script');
        scriptElement.textContent = scriptContent;
        document.body.appendChild(scriptElement);
    });

    test('should fetch and display FAQs on page load', async () => {
        // A chamada de API e a renderização acontecem no carregamento do script.
        // Precisamos esperar que as promessas (fetch, json, render) sejam resolvidas.
        await new Promise(process.nextTick);
        
        const rows = document.querySelectorAll('#faq-table-body tr');
        expect(rows.length).toBe(2);
        expect(rows[0].children[0].textContent).toBe('Q1');
        expect(rows[1].children[0].textContent).toBe('Q2');
    });

    test('should open modal to create a new FAQ', () => {
        document.getElementById('add-faq-button').click();
        
        const modal = document.getElementById('faq-modal');
        expect(modal.style.display).toBe('block');
    });

    test('should log out and redirect to login page', () => {
        document.getElementById('logout-button').click();
        
        expect(window.localStorage.getItem('access_token')).toBeNull();
        expect(window.location.href).toBe('login.html');
    });
});
