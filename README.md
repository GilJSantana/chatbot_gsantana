# 🚀 Chatbot Gsantana!

Este é o repositório principal do projeto **Chatbot Gjsantana**, um sistema de perguntas e respostas frequentes (FAQ) desenvolvido para auxiliar os visitantes do site do Lab Yes!. O projeto é construído com foco em uma arquitetura robusta e escalável, utilizando tecnologias modernas e as melhores práticas de desenvolvimento.

## ✨ Visão Geral

O Chatbot Gsantana visa aprimorar a experiência do usuário no site do Lab Yes!, fornecendo respostas rápidas e automatizadas para dúvidas comuns. Ele é projetado como uma API RESTful em Python com um frontend leve em JavaScript que pode ser facilmente integrado a qualquer página web.

## 📐 Arquitetura

A arquitetura do projeto segue o **Modelo C4**, descrevendo o sistema em diferentes níveis de abstração para garantir clareza e compreensão:

* **Diagrama de Contexto:** [docs/02-modelo-c4.md#1-nível-1-diagrama-de-contexto-do-sistema-system-context-diagram](docs/02-modelo-c4.md#1-nível-1-diagrama-de-contexto-do-sistema-system-context-diagram)
* **Diagrama de Contêineres:** [docs/02-modelo-c4.md#2-nível-2-diagrama-de-contêineres-container-diagram](docs/02-modelo-c4.md#2-nível-2-diagrama-de-contêineres-container-diagram)
* **Diagrama de Componentes:** [docs/02-modelo-c4.md#3-nível-3-diagrama-de-componentes-component-diagram---para-a-api-do-chatbot](docs/02-modelo-c4.md#3-nível-3-diagrama-de-componentes-component-diagram---para-a-api-do-chatbot)

Para detalhes completos e visuais dos diagramas, consulte o documento [Modelo C4 da Arquitetura](docs/02-modelo-c4.md).

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 🐍, FastAPI, Uvicorn
* **Banco de Dados:** PostgreSQL 🐘
* **Containerização:** Docker 🐳, Docker Compose
* **Frontend:** JavaScript, HTML, CSS (interface minimalista do chatbot)
* **Gerenciamento de Dependências:** Poetry
* **Versionamento:** Git
* **Documentação:** Markdown, Modelo C4

## 📦 Rodando o Projeto com Docker

A maneira recomendada para rodar o projeto localmente é utilizando Docker, que garante um ambiente consistente e isolado.

### Pré-requisitos

Certifique-se de ter instalado:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

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

- A aplicação estará disponível em `http://localhost`.
- A interface de administração estará em `http://localhost/admin`.
- A documentação interativa (Swagger UI) estará em `http://localhost/docs`.

---

## 🛠️ Gerenciamento de Usuários (CLI)

O projeto inclui uma ferramenta de linha de comando (`manage.py`) para gerenciar usuários de forma segura, especialmente em ambientes de produção.

**Importante:** Todos os comandos devem ser executados através do `docker-compose run`, que executa o script dentro de um contêiner temporário do serviço `api`, garantindo acesso ao banco de dados.

### Comandos Disponíveis

#### Inicializar o Banco de Dados
Cria todas as tabelas no banco de dados. Útil para a configuração inicial de um ambiente limpo.
```sh
docker-compose run --rm api python manage.py init-db
```

#### Criar um Usuário
Cria um novo usuário. Por padrão, cria um usuário comum. Use a flag `--admin` para criar um administrador.
```sh
docker-compose run --rm api python manage.py create-user <username> <email> [--admin]
```
**Exemplo (Usuário Comum):**
```sh
docker-compose run --rm api python manage.py create-user joao joao@example.com
```
**Exemplo (Administrador):**
```sh
docker-compose run --rm api python manage.py create-user gilmar admin@example.com --admin
```

#### Listar Usuários
Lista todos os usuários cadastrados no sistema, exibindo seus IDs, nomes de usuário, e-mails e status de administrador.
```sh
docker-compose run --rm api python manage.py list-users
```

#### Promover um Usuário
Concede privilégios de administrador a um usuário comum existente.
```sh
docker-compose run --rm api python manage.py promote-user <username>
```

#### Rebaixar um Usuário
Remove os privilégios de administrador de um usuário, tornando-o um usuário comum.
```sh
docker-compose run --rm api python manage.py demote-user <username>
```

### Níveis de Permissão

O sistema atualmente define dois níveis de permissão para os usuários:

**1. Administrador (`is_admin = True`)**

Usuários administradores têm acesso total às funcionalidades de gerenciamento do sistema.
*   **Gerenciamento de FAQs:** Acesso completo de CRUD (Criar, Ler, Atualizar, Deletar) através da API (`/api/v1/faqs/`) e da interface de administração.
*   **Acesso à Interface de Admin:** Acesso completo à seção `/admin`.

**2. Usuário Comum (`is_admin = False`)**

Usuários comuns (ou não autenticados) têm acesso apenas às funcionalidades públicas.
*   **Gerenciamento de FAQs:** **Nenhum acesso**. Todas as requisições para os endpoints de gerenciamento de FAQs serão bloqueadas com um erro `403 Forbidden`.
*   **Acesso ao Chat:** Podem interagir normalmente com o chatbot.

### Solução de Problemas

Se você encontrar problemas de autenticação ou de banco de dados, a maneira mais segura de recomeçar é apagar completamente o ambiente Docker e reconstruí-lo. Isso garante um banco de dados 100% limpo.

```sh
# Pare e apague os contêineres e os volumes de dados
docker-compose down -v

# Reconstrua as imagens sem usar cache e inicie os serviços
docker-compose up --build -d
```

## 🧪 Testes

Para executar os testes automatizados do projeto, utilize o `docker-compose` para rodar os testes no ambiente containerizado:

```bash
docker-compose run --rm api poetry run pytest
```

## 📄 Documentação Adicional

* [Especificação](docs/01-especificacao.md)
* [C4](docs/02-modelo-c4.md)
* [Decisões de Arquitetura](docs/03-arquitetura.md)
* [Considerações de Segurança](docs/04-seguranca.md)
* [Processo de Design (UX/UI)](docs/05-design.md)
* [Plano de Implantação](docs/06-deploy.md)
* [Guia de Uso](docs/07-guias-de-uso.md)

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1.  Faça um fork do projeto.
2.  Crie uma nova branch para sua funcionalidade ou correção (`git checkout -b feature/minha-nova-feature`).
3.  Faça suas alterações e adicione (`git add .`) e commite-as (`git commit -m 'feat: Adiciona nova funcionalidade X'`).
4.  Envie suas alterações para a nova branch (`git push origin feature/minha-nova-feature`).
5.  Abra um Pull Request no repositório original.


## 📞 Contato

* **Linkedin:** [Gilmar](https://www.linkedin.com/in/gilmarjs/)
* **Lab Yes!:** [https://Lab Yes!.com](https://lab-yes.com)

---
