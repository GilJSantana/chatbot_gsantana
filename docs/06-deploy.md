# 🚀 Plano de Implantação (Deploy) do Chatbot Gsantana

Este documento descreve o processo de implantação do Chatbot Gsantana, cobrindo os ambientes, as etapas necessárias para o *deploy* da API e do frontend, e as considerações para garantir uma transição bem-sucedida para o ambiente de produção.

## 1. Visão Geral da Estratégia de Deploy

A estratégia de implantação inicial do Chatbot Gsantana é um processo manual simples, ideal para a fase inicial do projeto. O plano contempla a implantação do backend (API) e do frontend em um ambiente de servidor web, com foco em simplicidade e controle.

* **Abordagem:** Implantação manual (`SSH`/`SCP` ou `git pull`).
* **Componentes:**
    * **Backend (API):** Executado como um processo de serviço (usando `systemd` ou similar) com Gunicorn e um servidor web reverso (como Nginx).
    * **Frontend:** Servido como arquivos estáticos pelo mesmo servidor web.

## 2. Ambientes de Implantação

O projeto considerará os seguintes ambientes:

* **Desenvolvimento (Dev):** O ambiente local de cada desenvolvedor. As instruções de execução estão no `README.md`.
* **Produção (Prod):** O ambiente final e público onde o chatbot estará disponível para os usuários.

## 3. Pré-requisitos do Servidor de Produção

Antes de iniciar a implantação, o servidor de produção deve ter os seguintes componentes instalados e configurados:

* **Sistema Operacional:** Linux (ex: Ubuntu Server, Debian).
* **Linguagem:** Python 3.8+
* **Gerenciamento de Dependências:** Poetry
* **Servidor WSGI:** Gunicorn
* **Servidor Web:** Nginx (para atuar como proxy reverso e servir o frontend)
* **Ferramentas:** Git, `pip` (para instalar o poetry).
* **Segurança:** Acesso SSH configurado com chaves públicas.

## 4. Etapas do Processo de Implantação

As seguintes etapas devem ser executadas no servidor de produção, idealmente por um usuário dedicado de sistema.

### Passo 1: Configuração Inicial

1.  Acesse o servidor via SSH.
2.  Clone o repositório do projeto em um diretório apropriado (ex: `/var/www/gsantana-chatbot/`).
    ```bash
    cd /var/www/
    git clone [https://github.com/seu-usuario/chatbot_gsantana.git](https://github.com/seu-usuario/chatbot_gsantana.git) gsantana-chatbot
    cd gsantana-chatbot
    ```
3.  Instale as dependências usando Poetry.
    ```bash
    poetry install --no-dev
    ```
    *(O `--no-dev` garante que apenas as dependências de produção sejam instaladas.)*

### Passo 2: Configuração do Backend (Gunicorn e Systemd)

1.  Crie um arquivo de serviço para o `systemd` (ex: `/etc/systemd/system/gsantana-api.service`) para gerenciar o processo da API.
    ```ini
    [Unit]
    Description=Gunicorn instance to serve the Gsantana API
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/var/www/gsantana-chatbot/
    ExecStart=/home/seu-usuario/.poetry/bin/poetry run gunicorn --workers 4 --bind unix:/tmp/gsantana.sock app:app
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
    *(Adapte o `ExecStart` com o caminho correto para o seu binário do Poetry e o nome do seu módulo/aplicação, ex: `app:app`.)*
2.  Habilite e inicie o serviço.
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start gsantana-api
    sudo systemctl enable gsantana-api
    ```

### Passo 3: Configuração do Frontend (Nginx)

1.  Crie um arquivo de configuração para o Nginx (ex: `/etc/nginx/sites-available/gsantana.conf`).
2.  Configure o Nginx para servir os arquivos estáticos do frontend e atuar como proxy reverso para a API.
    ```nginx
    server {
        listen 80;
        server_name chatbot.seu-dominio.com; # Substitua pelo seu domínio

        # Servir arquivos estáticos do frontend
        location / {
            root /var/www/gsantana-chatbot/frontend;
            index index.html;
        }

        # Proxy reverso para a API
        location /api {
            proxy_pass http://unix:/tmp/gsantana.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    ```
3.  Ative a configuração e reinicie o Nginx.
    ```bash
    sudo ln -s /etc/nginx/sites-available/gsantana.conf /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## 5. Plano de Rollback

Em caso de falha na implantação, as seguintes ações serão tomadas para restaurar a versão anterior:

* Reverter o código para o último *commit* estável usando Git: `git checkout <commit-id-estável>`
* Reiniciar os serviços `gsantana-api` e `nginx`.

## 6. Verificação Pós-Implantação

Após a conclusão das etapas, a implantação será verificada:

* Acesse `http://chatbot.seu-dominio.com` e verifique se a interface do chatbot é exibida corretamente.
* Interaja com o chatbot para garantir que as requisições à API (`/api/faq/search`) estão funcionando e retornando respostas válidas.
* Verifique os logs do Gunicorn (`sudo journalctl -u gsantana-api.service`) e do Nginx para garantir que não há erros.

## 7. Melhorias Futuras

Para aprimorar o processo de implantação, os seguintes passos são planejados:

* **CI/CD:** Implementar um pipeline de Integração Contínua e Entrega Contínua (CI/CD) usando GitHub Actions ou GitLab CI para automatizar testes e o deploy a cada *commit*.
* **Docker:** Conteinerizar a aplicação (backend e frontend) usando Docker para garantir portabilidade e ambientes de execução consistentes.
* **Orquestração:** Usar ferramentas como Docker Compose ou Kubernetes para gerenciar a implantação de contêineres e o escalonamento da aplicação.
* **Monitoramento:** Integrar um sistema de monitoramento (`Prometheus`, `Grafana`) e gerenciamento de logs (`ELK Stack`) para obter visibilidade em tempo real.

---