const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

describe('Admin Login Interface', () => {
    let document;
    let window;

    beforeEach(() => {
        const html = fs.readFileSync(path.resolve(__dirname, '../../html/admin/login.html'), 'utf8');
        const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost/admin/login.html' });
        
        window = dom.window;
        document = window.document;
        
        // Mock do localStorage
        Object.defineProperty(window, 'localStorage', {
            value: (function() {
                let store = {};
                return {
                    getItem: function(key) { return store[key] || null; },
                    setItem: function(key, value) { store[key] = value.toString(); },
                };
            })()
        });
        
        // Mock do fetch
        window.fetch = jest.fn();

        // Mock da navegação
        Object.defineProperty(window, 'location', {
            writable: true,
            value: { href: 'http://localhost/admin/login.html' }
        });

        // Carrega o script
        const scriptContent = fs.readFileSync(path.resolve(__dirname, '../../html/admin/js/login.js'), 'utf8');
        const scriptElement = document.createElement('script');
        scriptElement.textContent = scriptContent;
        document.body.appendChild(scriptElement);
    });

    test('should redirect to faqs.html on successful login', async () => {
        window.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ access_token: 'fake_token' }),
        });

        document.getElementById('login-form').dispatchEvent(new window.Event('submit'));
        await new Promise(process.nextTick);

        expect(window.localStorage.getItem('access_token')).toBe('fake_token');
        // Apenas verificamos se a navegação foi tentada
        expect(window.location.href).toBe('faqs.html');
    });

    test('should display error message on failed login', async () => {
        window.fetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({ detail: 'Credenciais inválidas' }),
        });

        document.getElementById('login-form').dispatchEvent(new window.Event('submit'));
        await new Promise(process.nextTick);

        const errorMessage = document.getElementById('error-message');
        expect(errorMessage.textContent).toBe('Credenciais inválidas');
        expect(errorMessage.style.display).toBe('block');
    });
});
