# 02 - Modelo C4 da Arquitetura do Chatbot

Este documento apresenta a arquitetura do chatbot do Lab-Yes utilizando o Modelo C4, que descreve software em diferentes níveis de abstração: Contexto do Sistema, Contêineres, Componentes e Código.

## 1. Nível 1: Diagrama de Contexto do Sistema (System Context Diagram)

O diagrama de contexto mostra o sistema que estamos construindo (o Chatbot do Lab-Yes) e como ele se encaixa em seu ambiente, identificando os usuários e os sistemas externos com os quais interage.

* **Objetivo:** Fornecer uma visão geral de alto nível do sistema, seus usuários e sistemas externos.
* **Elementos:**
    * **Pessoas:**
        * `Visitante do Site Lab-Yes`: Usuário principal que interage com o chatbot.
        * `Administrador do Lab-Yes`: Pessoa responsável por gerenciar as FAQs do chatbot (futuramente via um painel administrativo, por enquanto via API).
    * **Sistemas:**
        * `Site do Lab-Yes`: O website principal onde o chatbot será incorporado.
        * `Chatbot do Lab-Yes`: O sistema a ser construído.

* **Interações:**
    * `Visitante do Site Lab-Yes` **usa** `Site do Lab-Yes`.
    * `Visitante do Site Lab-Yes` **interage com** `Chatbot do Lab-Yes` (via interface no site).
    * `Chatbot do Lab-Yes` **é incorporado em** `Site do Lab-Yes`.
    * `Administrador do Lab-Yes` **gerencia** `Chatbot do Lab-Yes` (adiciona/edita FAQs).

  ![Diagrama de Contexto do Sistema](images/context.png)

## 2. Nível 2: Diagrama de Contêineres (Container Diagram)

O diagrama de contêineres mostra a arquitetura de alto nível do sistema, dividindo-o em "contêineres" tecnológicos (aplicações, bancos de dados, sistemas de arquivos, etc.) que rodam em processos separados e se comunicam entre si.

* **Elementos:**
    * `Visitante do Site Lab-Yes`: (Pessoa)
    * `Site do Lab-Yes`: (Sistema)
    * `Navegador do Visitante`: (Contêiner - Aplicação Frontend) - O navegador web que executa o JavaScript do chatbot.
    * `API do Chatbot (Flask)`: (Contêiner - Aplicação Backend) - Serviço Python/Flask que processa as mensagens e busca as respostas.
    * `Banco de Dados FAQ (SQLite)`: (Contêiner - Banco de Dados) - Armazena as perguntas e respostas frequentes.

* **Interações:**
    * `Visitante do Site Lab-Yes` **usa** `Navegador do Visitante`.
    * `Navegador do Visitante` **envia requisições HTTP (API)** para `API do Chatbot (Flask)`.
    * `API do Chatbot (Flask)` **lê/escreve dados** no `Banco de Dados FAQ (SQLite)`.
    * `Administrador do Lab-Yes` **gerencia (via API)** `API do Chatbot (Flask)`.
  



![Diagrama de Contêineres](images/container.png)

## 3. Nível 3: Diagrama de Componentes (Component Diagram - para a API do Chatbot)

Este nível foca em uma única caixa do diagrama de contêineres (a `API do Chatbot (Flask)`) e a decompõe em seus principais componentes internos.

* **Elementos (dentro da API do Chatbot - Flask):**
    * `Visitante do Site Lab-Yes`: (Pessoa)
    * `Navegador do Visitante`: (Contêiner)
    * `Servidor Web Gunicorn/Flask`: (Componente) - O ponto de entrada que lida com as requisições HTTP.
    * `Módulo de Rotas API`: (Componente) - Define os endpoints HTTP (ex: `/chat`, `/add_faq`).
    * `Serviço de FAQ (FAQService)`: (Componente) - Encapsula a lógica de negócio para buscar e processar FAQs.
    * `Repositório FAQ (FAQRepository)`: (Componente) - Abstrai a interação direta com o banco de dados (usando SQLAlchemy).
    * `Módulo de Validação de Entrada`: (Componente) - Garante que as requisições da API são válidas.
    * `Módulo de Logging`: (Componente) - Registra eventos e erros.
    * `Banco de Dados FAQ (SQLite)`: (Contêiner externo a este detalhe, mas interage com).

* **Interações:**
    * `Navegador do Visitante` **envia requisição HTTP** para `Servidor Web Gunicorn/Flask`.
    * `Servidor Web Gunicorn/Flask` **direciona** para `Módulo de Rotas API`.
    * `Módulo de Rotas API` **utiliza** `Módulo de Validação de Entrada`.
    * `Módulo de Rotas API` **chama** `Serviço de FAQ`.
    * `Serviço de FAQ` **utiliza** `Repositório FAQ`.
    * `Repositório FAQ` **interage com** `Banco de Dados FAQ (SQLite)`.
    * Todos os componentes **escrevem logs** no `Módulo de Logging`.

C4Component
    title Diagrama de Componentes para a API do Chatbot (Flask)

    Container(browser_app, "Aplicação Frontend (Navegador)", "JavaScript")
    ContainerDb(faq_database, "Banco de Dados FAQ (SQLite)")
    Person(administrator, "Administrador Lab-Yes")

    Component_Boundary(api_boundary, "API do Chatbot (Flask)") {
        Component(http_server, "Servidor HTTP (Gunicorn/Flask)", "Python", "Recebe e roteia as requisições HTTP.")
        Component(routes_module, "Módulo de Rotas API", "Python", "Define os endpoints da API (e.g., /chat, /add_faq).")
        Component(faq_service, "Serviço de FAQ (FAQService)", "Python", "Lógica de negócio para busca e processamento de FAQs.")
        Component(faq_repository, "Repositório FAQ (FAQRepository)", "Python, SQLAlchemy", "Abstrai a interação com o banco de dados para FAQs.")
        Component(input_validator, "Validador de Entrada", "Python", "Valida os dados de entrada das requisições (e.g., JSON payload).")
        Component(logger_component, "Componente de Logging", "Python", "Gerencia o registro de eventos e erros.")
    }

    Rel(browser_app, http_server, "Envia Requisições", "HTTP/HTTPS")
    Rel(administrator, routes_module, "Chama endpoints de administração", "HTTP/HTTPS")

    Rel(http_server, routes_module, "Roteia requisições")
    Rel(routes_module, input_validator, "Utiliza para validar entrada")
    Rel(routes_module, faq_service, "Chama lógica de negócio")
    Rel(faq_service, faq_repository, "Utiliza para acesso a dados")
    Rel(faq_repository, faq_database, "Lê/Escreve dados")

    Rel_U(http_server, logger_component, "Escreve logs")
    Rel_U(routes_module, logger_component, "Escreve logs")
    Rel_U(faq_service, logger_component, "Escreve logs")
