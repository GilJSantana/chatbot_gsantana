# 📚 Guias de Uso do Chatbot Gsantana

Este documento serve como um guia prático para interagir com o Chatbot Gsantana, tanto para usuários finais quanto para desenvolvedores e administradores que precisam interagir com a API.

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

### Exemplo de Endpoints

A seguir, alguns exemplos dos principais endpoints que você encontrará na documentação interativa.

#### **GET /api/v1/faq/search?q={query}**

*   **Descrição:** Busca por FAQs com base em uma consulta do usuário.
*   **Parâmetros de Query:**
    *   `q` (obrigatório): A pergunta do usuário.
*   **Exemplo de Resposta (200 OK):**

    ```json
    {
      "answer": "Somos um laboratório de testes genéticos focado em saúde e bem-estar.",
      "confidence": 0.92
    }
    ```

## 3. Guia de Administração da API

Os endpoints de administração são usados para gerenciar a base de conhecimento do chatbot. Em produção, eles **devem ser protegidos** por um sistema de autenticação (OAuth2/JWT).

#### **POST /api/v1/faq/**

*   **Descrição:** Adiciona uma nova pergunta e resposta (FAQ).
*   **Corpo da Requisição (JSON):**

    ```json
    {
      "question": "O que é o Lab-Yes?",
      "answer": "Somos um laboratório de testes genéticos."
    }
    ```

*   **Resposta (201 Created):** Confirmação da criação.

#### **PUT /api/v1/faq/{faq_id}**

*   **Descrição:** Edita uma FAQ existente com base no seu ID.
*   **Parâmetros de Rota:**
    *   `faq_id` (obrigatório): O ID da FAQ a ser editada.
*   **Corpo da Requisição (JSON):** Corpo da FAQ com os dados atualizados.

#### **DELETE /api/v1/faq/{faq_id}**

*   **Descrição:** Deleta uma FAQ da base de dados.
*   **Parâmetros de Rota:**
    *   `faq_id` (obrigatório): O ID da FAQ a ser deletada.

---