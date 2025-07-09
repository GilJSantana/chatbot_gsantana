# 🚀 Chatbot Lab-Yes

Este é o repositório principal do projeto **Chatbot Lab-Yes**, um sistema de perguntas e respostas frequentes (FAQ) desenvolvido para auxiliar os visitantes do site do Lab-Yes. O projeto é construído com foco em uma arquitetura robusta e escalável, utilizando tecnologias modernas e as melhores práticas de desenvolvimento.

## ✨ Visão Geral

O Chatbot Lab-Yes visa aprimorar a experiência do usuário no site do Lab-Yes, fornecendo respostas rápidas e automatizadas para dúvidas comuns. Ele é projetado como uma API RESTful em Python (Flask) com um frontend leve em JavaScript que pode ser facilmente integrado a qualquer página web.

## 📐 Arquitetura

A arquitetura do projeto segue o **Modelo C4**, descrevendo o sistema em diferentes níveis de abstração para garantir clareza e compreensão:

* **Diagrama de Contexto:** [docs/02-modelo-c4.md#1-nível-1-diagrama-de-contexto-do-sistema-system-context-diagram](docs/02-modelo-c4.md#1-nível-1-diagrama-de-contexto-do-sistema-system-context-diagram)
* **Diagrama de Contêineres:** [docs/02-modelo-c4.md#2-nível-2-diagrama-de-contêineres-container-diagram](docs/02-modelo-c4.md#2-nível-2-diagrama-de-contêineres-container-diagram)
* **Diagrama de Componentes:** [docs/02-modelo-c4.md#3-nível-3-diagrama-de-componentes-component-diagram---para-a-api-do-chatbot](docs/02-modelo-c4.md#3-nível-3-diagrama-de-componentes-component-diagram---para-a-api-do-chatbot)

Para detalhes completos e visuais dos diagramas, consulte o documento [Modelo C4 da Arquitetura](docs/02-modelo-c4.md).

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 🐍, Flask, Gunicorn
* **Banco de Dados:** SQLite (para gerenciamento de FAQs)
* **Frontend:** JavaScript, HTML, CSS (interface minimalista do chatbot)
* **Gerenciamento de Dependências:** Poetry
* **Versionamento:** Git
* **Documentação:** Markdown, Modelo C4

## 📦 Como Rodar o Projeto (Desenvolvimento)

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local:

### Pré-requisitos

Certifique-se de ter instalado:

* [Python 3.8+](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de dependências e pacotes Python)

    Para instalar o Poetry, use o comando recomendado para seu sistema operacional (geralmente):
    ```bash
    # No macOS / Linux / WSL
    curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -

    # No Windows (PowerShell)
    (Invoke-WebRequest -Uri [https://install.python-poetry.org](https://install.python-poetry.org) -UseBasicParsing).Content | python -
    ```
    Após a instalação, certifique-se de que o Poetry esteja no seu PATH.

### Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/chatbot_lab_yes.git](https://github.com/seu-usuario/chatbot_lab_yes.git)
    cd chatbot_lab_yes
    ```

2.  **Instale as dependências usando Poetry:**
    O Poetry criará automaticamente um ambiente virtual e instalará todas as dependências definidas no `pyproject.toml`.
    ```bash
    poetry install
    ```

3.  **Ative o ambiente virtual do Poetry:**
    ```bash
    poetry shell
    ```
    *Obs: Você estará agora dentro do ambiente virtual. Todos os comandos Python a seguir usarão as dependências instaladas pelo Poetry.*

4.  **Inicialize o banco de dados e adicione dados de exemplo (opcional):**
    ```bash
    python -c "from app import db; db.create_all()"
    python scripts/populate_db.py # Se você tiver um script para popular o DB
    ```
    *Obs: Você precisará criar o `scripts/populate_db.py` ou incluir a lógica de população no `app.py` para esta etapa funcionar.*

5.  **Inicie a API do Chatbot:**
    ```bash
    flask run
    # ou se estiver usando Gunicorn (recomendado para produção)
    # gunicorn -w 4 app:app
    ```
    A API estará disponível em `http://127.0.0.1:5000` por padrão.

6.  **Execute o Frontend:**
    Abra o arquivo `frontend/index.html` (ou o nome do seu arquivo HTML principal) em seu navegador para ver a interface do chatbot. Você pode precisar de um pequeno servidor HTTP local (como `python -m http.server` na pasta `frontend` ou usar as ferramentas de desenvolvimento do seu navegador) se o seu frontend fizer requisições AJAX e tiver problemas com restrições de CORS ao abrir o arquivo diretamente.

## 🧪 Testes


Para executar os testes automatizados do projeto:

```bash
poetry run pytest # Exemplo para pytest
# ou
poetry run python -m unittest discover # Exemplo para unittest