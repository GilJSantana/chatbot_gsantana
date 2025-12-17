# 📚 Guias de Uso do Chatbot Gsantana

Este documento serve como um guia prático para interagir com o Chatbot Gsantana, tanto para usuários finais quanto para desenvolvedores e administradores.

## 1. Guia para o Usuário Final (Visitantes do Site)

O Chatbot Gsantana foi projetado para ser intuitivo e fácil de usar.

*   **Acesso:** O chatbot pode ser acessado através de um ícone flutuante no canto da página.
*   **Interface:** A interface é um chat simples. Digite sua pergunta no campo de texto e pressione "Enter" ou clique no botão de envio.
*   **Respostas:** O chatbot buscará a resposta mais relevante em sua base de conhecimento. Se não encontrar, informará e sugerirá reformular a pergunta ou entrar em contato por outros meios.

## 2. Guia de Acesso à API para Desenvolvedores

A API do Chatbot Gsantana é construída com FastAPI, o que nos fornece uma documentação interativa e sempre atualizada.

### Documentação Interativa (Swagger UI)

A forma recomendada de explorar e testar a API é através da documentação interativa gerada automaticamente, disponível na rota `/docs`.

*   **URL (Desenvolvimento Local):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Nesta página, você pode ver todos os endpoints disponíveis, seus parâmetros, schemas de requisição/resposta e até mesmo enviar requisições de teste diretamente do seu navegador.

### Documentação Alternativa (ReDoc)

Uma visão alternativa da documentação, mais focada na leitura, está disponível na rota `/redoc`.

*   **URL (Desenvolvimento Local):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 3. Guia de Administração (Web)

A administração da base de conhecimento do chatbot (FAQs) é realizada através de uma interface web de administração.

*   **Acesso:** A interface de administração está disponível na rota `/admin/`.
    *   **URL (Desenvolvimento Local):** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
*   **Autenticação:** O acesso é protegido e requer credenciais de superusuário.
*   **Gerenciando FAQs:**
    *   **Listar:** Após o login, clique em "FAQs" para ver todas as perguntas e respostas cadastradas.
    *   **Adicionar:** Clique em "Adicionar FAQ", preencha os campos e salve.
    *   **Editar/Remover:** Clique em uma FAQ existente para abrir a tela de edição, onde você pode alterar os dados ou remover o registro.

---