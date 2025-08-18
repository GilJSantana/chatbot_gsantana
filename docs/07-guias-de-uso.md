Este documento serve como um guia prático para interagir com o Chatbot Gsantana. Ele detalha como usar a interface do chatbot e fornece a documentação dos endpoints da API para desenvolvedores e administradores.

## 1. Guia para o Usuário Final (Visitantes do Site)

O Chatbot Gsantana é projetado para ser intuitivo e fácil de usar.

* **Acesso:** O chatbot pode ser acessado através de um ícone flutuante ou um componente incorporado em uma página do site do Lab-Yes.
* **Interface:** A interface do usuário é um chat simples. Digite sua pergunta no campo de texto e pressione "Enter" ou clique no botão de envio.
* **Respostas:** O chatbot tentará encontrar a resposta mais relevante para sua pergunta com base na base de dados de FAQs. As respostas serão exibidas no chat.
* **Limitações:** O chatbot está focado em perguntas frequentes. Para questões mais complexas, um contato direto com a equipe de suporte do Lab-Yes pode ser necessário.

## 2. Guia de Acesso à API para Desenvolvedores

Esta seção é dedicada a desenvolvedores que precisam interagir com a API do Chatbot Gsantana diretamente.

### URL Base da API

http://127.0.0.1:5000/api

*(Para uso em desenvolvimento local. A URL base em produção pode ser diferente.)*

### Endpoints da API

#### **GET /api/faq/search?q=<query>**

* **Descrição:** Busca por perguntas e respostas (FAQs) com base em uma string de consulta.
* **Método:** `GET`
* **Parâmetros de Query:**
    * `q` (obrigatório): A string de texto a ser usada para a busca (a pergunta do usuário).
* **Resposta (Sucesso - Código 200 OK):**
    * **Corpo da Resposta:** Um objeto JSON contendo a resposta encontrada ou uma mensagem de "não encontrado".
    * **Exemplo de Resposta:**
        ```json
        {
          "answer": "Nós somos um laboratório de testes genéticos focado em saúde e bem-estar. Oferecemos uma variedade de testes para diversas necessidades.",
          "confidence": 0.85
        }
        ```
* **Resposta (Falha - Código 404 Not Found):**
    * **Corpo da Resposta:** Um objeto JSON com uma mensagem de erro.
    * **Exemplo de Resposta:**
        ```json
        {
          "error": "Nenhuma resposta relevante encontrada para sua pergunta."
        }
        ```

---

## 3. Guia de Administração da API

Esta seção detalha como um administrador pode gerenciar a base de dados de FAQs através dos endpoints da API.

* **Aviso de Segurança:** Estes endpoints de administração **devem** ser protegidos por um sistema de autenticação (como um token JWT) em um ambiente de produção para evitar acesso não autorizado. No ambiente de desenvolvimento, a proteção pode ser mais simples.

### Endpoints de Administração

#### **POST /api/faq/add**

* **Descrição:** Adiciona uma nova pergunta e resposta (FAQ) à base de dados.
* **Método:** `POST`
* **Corpo da Requisição (JSON):**
    ```json
    {
      "question": "O que é o Lab-Yes?",
      "answer": "Nós somos um laboratório de testes genéticos focado em saúde e bem-estar. Oferecemos uma variedade de testes para diversas necessidades."
    }
    ```
* **Resposta (Sucesso - Código 201 Created):**
    * **Corpo da Resposta:** Um objeto JSON confirmando o sucesso.
    * **Exemplo de Resposta:**
        ```json
        {
          "message": "FAQ adicionada com sucesso.",
          "question": "O que é o Lab-Yes?"
        }
        ```

#### **PUT /api/faq/edit/<faq_id>**

* **Descrição:** Edita uma FAQ existente com base no seu ID.
* **Método:** `PUT`
* **Parâmetros de Rota:**
    * `<faq_id>` (obrigatório): O ID da FAQ a ser editada.
* **Corpo da Requisição (JSON):**
    ```json
    {
      "question": "O que é o Lab-Yes?",
      "answer": "Somos um laboratório de análises genéticas, fornecendo serviços de teste para saúde e bem-estar."
    }
    ```
* **Resposta (Sucesso - Código 200 OK):**
    * **Corpo da Resposta:** Um objeto JSON confirmando a edição.
* **Resposta (Falha - Código 404 Not Found):**
    * **Corpo da Resposta:** Uma mensagem de erro.

#### **DELETE /api/faq/delete/<faq_id>**

* **Descrição:** Deleta uma FAQ da base de dados.
* **Método:** `DELETE`
* **Parâmetros de Rota:**
    * `<faq_id>` (obrigatório): O ID da FAQ a ser deletada.
* **Resposta (Sucesso - Código 200 OK):**
    * **Corpo da Resposta:** Um objeto JSON confirmando a exclusão.
* **Resposta (Falha - Código 404 Not Found):**
    * **Corpo da Resposta:** Uma mensagem de erro.

---