# Modelo C4 da Arquitetura do Chatbot

Este documento apresenta a arquitetura do chatbot Gsantana utilizando o Modelo C4, que descreve software em diferentes níveis de abstração: Contexto do Sistema, Contêineres, Componentes e Código.

## 1. Nível 1: Diagrama de Contexto do Sistema (System Context Diagram)

O diagrama de contexto mostra o sistema que estamos construindo (o Chatbot do Gsantana) e como ele se encaixa em seu ambiente, identificando os usuários e os sistemas externos com os quais interage.

* **Objetivo:** Fornecer uma visão geral de alto nível do sistema, seus usuários e sistemas externos.
* **Elementos:**
    * **Pessoas:**
        * `Visitante do Site Lab-Yes`: Usuário principal que interage com o chatbot.
        * `Administrador do Lab-Yes`: Pessoa responsável por gerenciar as FAQs do chatbot através da interface de administração.
    * **Sistemas:**
        * `Site do Lab-Yes`: O website principal onde o chatbot será incorporado.
        * `Chatbot Gsantana`: O sistema a ser construído.

* **Interações:**
    * `Visitante do Site Lab-Yes` **usa** `Site do Lab-Yes`.
    * `Visitante do Site Lab-Yes` **interage com** `Chatbot Gsantana` (via interface no site).
    * `Chatbot Gsantana` **é incorporado em** `Site do Lab-Yes`.
    * `Administrador do Lab-Yes` **gerencia** `Chatbot Gsantana` (adiciona/edita FAQs).
       
        ![Diagrama de Contexto do Sistema](https://raw.githubusercontent.com/gilunix/chatbot_gsantana/main/docs/images/context.png)

## 2. Nível 2: Diagrama de Contêineres (Container Diagram)

O diagrama de contêineres mostra a arquitetura de alto nível do sistema, dividindo-o em "contêineres" tecnológicos (aplicações, bancos de dados, sistemas de arquivos, etc.) que rodam em processos separados e se comunicam entre si.

* **Elementos:**
    * `Visitante do Site Lab-Yes`: (Pessoa)
    * `Administrador do Lab-Yes`: (Pessoa)
    * `Site do Lab-Yes`: (Sistema)
    * `Navegador do Visitante/Admin`: (Contêiner - Aplicação Frontend) - O navegador web que executa o JavaScript do chatbot ou a interface de administração.
    * `API do Chatbot (FastAPI)`: (Contêiner - Aplicação Backend) - Serviço Python/FastAPI que processa as mensagens, busca as respostas e serve a interface de administração.
    * `Banco de Dados (SQLite/PostgreSQL)`: (Contêiner - Banco de Dados) - Armazena as FAQs e outros dados da aplicação.

* **Interações:**
    * `Visitante do Site Lab-Yes` **usa** o `Navegador` para interagir com o widget do chatbot.
    * `Navegador` (widget) **envia requisições HTTP (API)** para a `API do Chatbot (FastAPI)`.
    * `Administrador do Lab-Yes` **usa** o `Navegador` para acessar a interface de administração servida pela `API do Chatbot (FastAPI)`.
    * `API do Chatbot (FastAPI)` **lê/escreve dados** no `Banco de Dados`.
        ![Diagrama de Contêineres](https://raw.githubusercontent.com/gilunix/chatbot_gsantana/main/docs/images/container.png)
        *(Nota: O diagrama usa Flask como exemplo, mas a implementação atual utiliza FastAPI).*

## 3. Nível 3: Diagrama de Componentes (Component Diagram - para a API do Chatbot)

Este nível foca em uma única caixa do diagrama de contêineres (a `API do Chatbot (FastAPI)`) e a decompõe em seus principais componentes internos.

* **Elementos (dentro da API do Chatbot - FastAPI):**
    * `Servidor Web ASGI (Uvicorn)`: (Componente) - O ponto de entrada que lida com as requisições HTTP.
    * `Módulo de Rotas API (Routers)`: (Componente) - Define os endpoints HTTP (ex: `/chat`) usando os decoradores do FastAPI.
    * `Módulo de Administração (Admin)`: (Componente) - Gera e serve a interface de administração web para o gerenciamento de FAQs e outros modelos.
    * `Serviço de FAQ (FAQService)`: (Componente) - Encapsula a lógica de negócio para buscar e processar FAQs.
    * `Repositório (Repository)`: (Componente) - Abstrai a interação direta com o banco de dados (usando SQLAlchemy).
    * `Módulo de Validação (Pydantic)`: (Componente) - Garante que as requisições da API e os dados de resposta sigam um schema definido.
    * `Módulo de Logging`: (Componente) - Registra eventos e erros.
    * `Banco de Dados`: (Contêiner externo a este detalhe, mas interage com).

* **Interações:**
    * O `Navegador` **envia requisição HTTP** para o `Servidor Web ASGI (Uvicorn)`.
    * O `Servidor Web ASGI (Uvicorn)` **direciona** para o `Módulo de Rotas API` ou para o `Módulo de Administração`.
    * Os `Módulos de Rotas e Admin` **utilizam** o `Módulo de Validação (Pydantic)`.
    * Os `Módulos de Rotas e Admin` **chamam** `Serviços` (como o `FAQService`).
    * Os `Serviços` **utilizam** `Repositórios`.
    * Os `Repositórios` **interagem com** o `Banco de Dados`.
    * Todos os componentes **escrevem logs** no `Módulo de Logging`.

      ![Diagrama de componentes](https://raw.githubusercontent.com/gilunix/chatbot_gsantana/main/docs/images/diagrama.png)
      *(Nota: O diagrama usa Flask como exemplo, mas a implementação atual utiliza FastAPI e Uvicorn).*
