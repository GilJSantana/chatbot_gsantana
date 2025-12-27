# Interface de Administração de FAQs

Esta documentação descreve a interface de administração para gerenciar as Perguntas Frequentes (FAQs) do chatbot.

## Guia de Usuário

A interface de administração de FAQs permite que usuários autorizados criem, editem, e removam perguntas e respostas que o chatbot utiliza.

### Acesso à Interface

1.  Acesse a interface de administração através da URL: `http://localhost:8000/admin/`.
2.  Faça login com suas credenciais de superusuário.

### Gerenciando FAQs

-   **Criar uma nova FAQ:**
    1.  Na página principal do admin, clique em "FAQs".
    2.  Clique no botão "Adicionar FAQ".
    3.  Preencha os campos "Pergunta", "Resposta", e "Categoria".
    4.  Clique em "Salvar".

-   **Editar uma FAQ existente:**
    1.  Na lista de FAQs, clique na pergunta que deseja editar.
    2.  Modifique os campos necessários.
    3.  Clique em "Salvar".

-   **Remover uma FAQ:**
    1.  Na lista de FAQs, selecione as perguntas que deseja remover.
    2.  No menu de ações, selecione "Remover FAQs selecionadas".
    3.  Clique em "Ir".

## Detalhes Técnicos

A interface de administração é construída com o admin do FastAPI, que gera automaticamente uma interface web para os modelos de dados da aplicação.

### Endpoints Protegidos

Os endpoints de administração de FAQs são protegidos e requerem autenticação de superusuário. A autenticação é gerenciada pelo sistema de usuários do FastAPI.

### Fluxo de Autenticação

1.  O usuário acessa a página de login do admin.
2.  O usuário insere suas credenciais (usuário e senha).
3.  O backend verifica as credenciais e, se válidas, cria uma sessão para o usuário.
4.  O usuário é redirecionado para a interface de administração.

### Interação Frontend-Backend

A interface de administração gerada pelo FastAPI se comunica com o backend através de uma API RESTful para realizar as operações de CRUD (Create, Read, Update, Delete) no modelo de dados `FAQ`.
