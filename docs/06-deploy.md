# 🚀 Plano de Implantação (Deploy) do Chatbot Gsantana

Este documento descreve o processo de implantação do Chatbot Gsantana, com foco em uma estratégia moderna e automatizada usando Docker e CI/CD, alinhada com as melhores práticas de engenharia de software.

## 1. Visão Geral da Estratégia de Deploy

A estratégia de implantação do Chatbot Gsantana é baseada em **conteinerização com Docker e automação com CI/CD (GitHub Actions)**. Isso garante consistência, reprodutibilidade e agilidade no processo de deploy.

*   **Abordagem Principal:** Deploy automatizado via pipeline de CI/CD.
*   **Componentes Conteinerizados:**
    *   **Backend (API FastAPI):** Empacotado em uma imagem Docker.
    *   **Frontend (Estático):** Servido por um web server leve (como Nginx) em uma imagem Docker.
    *   **Banco de Dados:** Utilização de uma imagem oficial do PostgreSQL para produção.
*   **Orquestração:** `docker-compose` será usado para gerenciar os contêineres em ambientes de desenvolvimento e produção.

## 2. Ambientes de Implantação

*   **Desenvolvimento (Local):** Executado via `docker-compose` na máquina do desenvolvedor. Utilizará SQLite para simplicidade e hot-reloading para o código da API.
*   **Produção (Servidor Remoto):** Executado via `docker-compose` em um servidor de produção. Utilizará PostgreSQL e imagens otimizadas para produção.

## 3. Estratégia de CI/CD com GitHub Actions

Um pipeline de CI/CD será configurado no diretório `.github/workflows/` do repositório. O fluxo de trabalho será acionado a cada `push` na branch `main` e executará os seguintes passos:

1.  **Checkout do Código:** Baixa o código-fonte do repositório.
2.  **Lint & Test:** Executa os linters (Black, Flake8) e os testes automatizados (Pytest) para garantir a qualidade do código.
3.  **Build das Imagens Docker:** Constrói as imagens Docker para o backend e o frontend.
4.  **Push para o Docker Hub:** Envia as imagens construídas para um registro de contêineres (Docker Hub ou similar).
5.  **Deploy no Servidor de Produção:** Conecta-se ao servidor de produção via SSH e executa um script que:
    *   Faz o `pull` das novas imagens do Docker Hub.
    *   Reinicia os serviços usando `docker-compose up -d`.

## 4. Gerenciamento de Configuração

*   **Variáveis de Ambiente:** Todas as configurações específicas de cada ambiente (desenvolvimento, produção) serão gerenciadas por meio de arquivos `.env`.
*   **Exemplo de `.env` para produção:**

    ```
    # Configuração do Banco de Dados
    POSTGRES_USER=user
    POSTGRES_PASSWORD=secret
    POSTGRES_SERVER=db
    POSTGRES_DB=chatbot_db
    DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}/${POSTGRES_DB}

    # Configuração da Aplicação
    ALLOWED_ORIGINS=["https://www.lab-yes.com"]
    ```

    O arquivo `.env` de produção será criado manualmente no servidor e nunca será comitado no repositório Git.

## 5. Plano de Rollback

Em caso de falha na implantação, o rollback pode ser feito de duas maneiras:

*   **CI/CD:** Re-executar o pipeline para uma tag/commit anterior que estava estável.
*   **Manual:** Conectar ao servidor, alterar a tag da imagem no arquivo `docker-compose.prod.yml` para a versão anterior e reiniciar os serviços.

## 6. Verificação Pós-Implantação

*   Acessar a URL da aplicação e verificar se o frontend carrega.
*   Interagir com o chatbot para confirmar que a API está respondendo corretamente.
*   Verificar os logs dos contêineres em execução com `docker-compose logs` para garantir que não há erros.

## (Alternativa) Processo de Implantação Manual

Este processo pode ser usado para setups mais simples ou como um fallback. **Não é a abordagem recomendada.**

1.  **Pré-requisitos:** Servidor com Python, Poetry e Uvicorn instalados.
2.  **Código:** Clone ou puxe a versão mais recente do código com `git`.
3.  **Dependências:** Instale as dependências com `poetry install --no-dev`.
4.  **Execução:** Inicie a API com Uvicorn. Para produção, é recomendado usar um gerenciador de processos como `systemd`.
    *   **Exemplo de comando Uvicorn:**
        ```bash
        poetry run uvicorn src.chatbot_gsantana.main:app --host 0.0.0.0 --port 8000 --workers 4
        ```
    *   É necessário configurar um proxy reverso (como Nginx) na frente do Uvicorn para gerenciar HTTPS e servir os arquivos estáticos do frontend.

---