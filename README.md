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

### 1. Construir e Iniciar os Contêineres

Execute o seguinte comando na raiz do projeto. Este comando irá construir as imagens Docker, criar um banco de dados limpo e iniciar a aplicação.

```sh
docker-compose up --build -d
```

- A aplicação estará disponível em `http://localhost:8000`.
- A documentação interativa (Swagger UI) estará em `http://localhost:8000/docs`.

---

## 🛠️ Primeiros Passos: Criando um Superusuário e Autenticando

Para interagir com os endpoints protegidos (criar, editar, deletar FAQs), você precisa primeiro criar um usuário administrador e obter um token de autenticação.

### 1. Criar o Superusuário

O projeto inclui um script para criar um usuário administrador de forma interativa.

a. **Acesse o contêiner da API:**
   Primeiro, encontre o nome do seu contêiner da API:
   ```sh
   docker-compose ps
   ```
   (O nome será algo como `chatbot_gsantana-api-1`)

   Em seguida, acesse o terminal do contêiner:
   ```sh
   docker exec -it [NOME_DO_SEU_CONTAINER_API] bash
   ```

b. **Execute o script de criação:**
   Dentro do contêiner, execute o seguinte comando:
   ```sh
   python /app/scripts/create_superuser.py
   ```

c. **Siga as instruções:**
   O script pedirá seu `nome de usuário`, `email` e `senha` (com confirmação). Preencha com os dados desejados.

### 2. Autenticar na API via Swagger UI

a. **Acesse a documentação:**
   Abra seu navegador e vá para `http://localhost:8000/docs`.

b. **Obtenha o Token de Acesso:**
   - Encontre a seção **`Authentication`** e expanda o endpoint `POST /api/v1/auth/token`.
   - Clique em **"Try it out"**.
   - Preencha os campos `username` e `password` com as credenciais que você acabou de criar.
   - Clique em **"Execute"**.
   - Na resposta, copie o valor completo do `access_token`.

c. **Autorize o Swagger UI:**
   - No canto superior direito da página, clique no botão **"Authorize"**.
   - Na janela que abrir, no campo "Value", cole o token que você copiou, **prefixado com `Bearer ` e um espaço**.
     - Exemplo: `Bearer eyJhbGciOiJIUzI1Ni...`
   - Clique em **"Authorize"** e depois em **"Close"**.

Agora você está autenticado e pode testar todos os endpoints protegidos da API diretamente pelo Swagger.

### Solução de Problemas

Se você encontrar problemas de autenticação ou de banco de dados, a maneira mais segura de recomeçar é apagar completamente o ambiente Docker e reconstruí-lo. Isso garante um banco de dados 100% limpo.

```sh
# Pare e apague os contêineres e os volumes de dados
docker-compose down --volumes

# Reconstrua as imagens sem usar cache e inicie os serviços
docker-compose up --build --no-cache -d
```
Depois, repita o passo de criação do superusuário.

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
