document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const passwordInput = document.getElementById('password');
    const togglePassword = document.getElementById('toggle-password');

    // Lógica para mostrar/esconder a senha
    togglePassword.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        // Altera o ícone (opcional, mas melhora a UX)
        togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
    });

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        errorMessage.style.display = 'none';

        const username = document.getElementById('username').value;
        const password = passwordInput.value;

        try {
            const response = await fetch('/api/v1/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: username,
                    password: password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                window.location.href = 'faqs.html';
            } else {
                const errorData = await response.json();
                errorMessage.textContent = errorData.detail || 'Falha no login. Verifique suas credenciais.';
                errorMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Erro ao tentar fazer login:', error);
            errorMessage.textContent = 'Erro de conexão. Tente novamente mais tarde.';
            errorMessage.style.display = 'block';
        }
    });
});
