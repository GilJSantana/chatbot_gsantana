# 🚀 Chatbot Gsantana

[![CI/CD Pipeline](https://github.com/gilunix/chatbot_gsantana/actions/workflows/ci.yml/badge.svg)](https://github.com/gilunix/chatbot_gsantana/actions/workflows/ci.yml)
[![Sync Wiki](https://github.com/gilunix/chatbot_gsantana/actions/workflows/wiki-sync.yml/badge.svg)](https://github.com/gilunix/chatbot_gsantana/actions/workflows/wiki-sync.yml)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue?logo=docker)](https://github.com/gilunix/chatbot_gsantana/pkgs/container/chatbot_gsantana)

Este é o repositório principal do projeto **Chatbot Gsantana**, um sistema de perguntas e respostas frequentes (FAQ) desenvolvido para auxiliar os visitantes do site do Lab Yes!. O projeto é construído com foco em uma arquitetura robusta e escalável, utilizando tecnologias modernas e as melhores práticas de desenvolvimento.

## ✨ Visão Geral

O Chatbot Gsantana visa aprimorar a experiência do usuário no site do Lab Yes!, fornecendo respostas rápidas e automatizadas para dúvidas comuns. Ele é projetado como uma API RESTful em Python com um frontend leve em JavaScript que pode ser facilmente integrado a qualquer página web.

## 📚 Documentação Completa (Wiki)

Toda a documentação técnica, de arquitetura e guias de uso foi centralizada na **Wiki do GitHub**. Consulte os links abaixo para detalhes:

*   **[🏠 Home da Wiki](https://github.com/gilunix/chatbot_gsantana/wiki)**
*   **[Especificação do Projeto](https://github.com/gilunix/chatbot_gsantana/wiki/Especificacao-do-Projeto)**
*   **[Arquitetura do Sistema](https://github.com/gilunix/chatbot_gsantana/wiki/Arquitetura-do-Sistema)**
*   **[Modelo C4](https://github.com/gilunix/chatbot_gsantana/wiki/Modelo-C4)**
*   **[Guias de Uso](https://github.com/gilunix/chatbot_gsantana/wiki/Guias-de-Uso)**
*   **[Interface Administrativa](https://github.com/gilunix/chatbot_gsantana/wiki/Interface-Administrativa)**

## 🚀 Tecnologias Utilizadas

*   **Backend:** Python 🐍, FastAPI, Uvicorn
*   **Banco de Dados:** PostgreSQL 🐘
*   **Containerização:** Docker 🐳, Docker Compose
*   **Frontend:** JavaScript, HTML, CSS (interface minimalista do chatbot)
*   **CI/CD:** GitHub Actions, GitHub Container Registry (GHCR)
*   **Gerenciamento de Dependências:** Poetry

## 📦 Rodando o Projeto com Docker

A maneira recomendada para rodar o projeto localmente é utilizando Docker, que garante um ambiente consistente e isolado.

### Pré-requisitos

Certifique-se de ter instalado:
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Configuração do Ambiente

O projeto utiliza um arquivo `.env.e2e` para gerenciar as variáveis de ambiente para o ambiente Docker.

a. **Copie o Arquivo de Exemplo:**
   Na raiz do projeto, copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env.e2e`.
   ```sh
   cp .env.example .env.e2e
   ```

b. **Preencha o Arquivo `.env.e2e`:**
   Abra o arquivo `.env.e2e` e preencha **todas** as variáveis. Siga as instruções contidas nele para gerar a `SECRET_KEY` e defina os parâmetros do banco de dados. Adicione também as credenciais para o usuário administrador de teste (`TEST_ADMIN_USERNAME`, `TEST_ADMIN_PASSWORD`, etc.).

### 2. Construir e Iniciar os Contêineres

Execute o seguinte comando na raiz do projeto. Ele irá construir as imagens, criar as tabelas no banco de dados, criar o usuário administrador inicial e iniciar a aplicação.

```sh
docker-compose up --build -d
```

-   A aplicação estará disponível em `http://localhost`.
-   A interface de administração estará em `http://localhost/admin`.
-   A documentação interativa (Swagger UI) estará em `http://localhost/docs`.

---

## 🛠️ Gerenciamento de Usuários (CLI)

O projeto inclui uma ferramenta de linha de comando (`manage.py`) para gerenciar usuários de forma segura.

**Importante:** Todos os comandos devem ser executados através do `docker-compose run`.

### Comandos Disponíveis

#### Inicializar o Banco de Dados
```sh
docker-compose run --rm api python manage.py init-db
```

#### Criar um Usuário
```sh
docker-compose run --rm api python manage.py create-user <username> <email> [--admin]
```

#### Listar Usuários
```sh
docker-compose run --rm api python manage.py list-users
```

#### Promover/Rebaixar Usuário
```sh
docker-compose run --rm api python manage.py promote-user <username>
docker-compose run --rm api python manage.py demote-user <username>
```

## 🧪 Testes

Para executar os testes automatizados do projeto:

```bash
docker-compose run --rm api poetry run pytest
```

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1.  Faça um fork do projeto.
2.  Crie uma nova branch para sua funcionalidade ou correção (`git checkout -b feature/minha-nova-feature`).
3.  Faça suas alterações e adicione (`git add .`) e commite-as (`git commit -m 'feat: Adiciona nova funcionalidade X'`).
4.  Envie suas alterações para a nova branch (`git push origin feature/minha-nova-feature`).
5.  Abra um Pull Request no repositório original.

## 📞 Contato

*   **Linkedin:** [Gilmar](https://www.linkedin.com/in/gilmarjs/)
*   **Lab Yes!:** [https://lab-yes.com](https://lab-yes.com)

---
