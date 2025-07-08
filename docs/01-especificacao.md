# 01 - Especificação do Chatbot para Lab-Yes

## 1. Introdução

Este documento detalha as especificações funcionais e não-funcionais para o desenvolvimento de um chatbot de Perguntas Frequentes (FAQ) para o website do Lab-Yes (https://www.lab-yes.com). O objetivo principal é fornecer uma ferramenta de autoatendimento para os visitantes do site, otimizando a obtenção de informações e reduzindo a carga de trabalho de resposta manual.

## 2. Problema a Ser Resolvido

Atualmente, o Lab-Yes recebe diversas perguntas repetitivas de visitantes e potenciais voluntários através de e-mail e formulários de contato. Isso demanda tempo da equipe para responder a consultas comuns, que poderiam ser automatizadas.

## 3. Objetivos do Projeto

* **Otimizar o Atendimento:** Prover respostas imediatas para perguntas frequentes.
* **Reduzir Carga Operacional:** Diminuir o volume de e-mails e mensagens de contato sobre tópicos rotineiros.
* **Melhorar Experiência do Usuário:** Oferecer um canal de comunicação rápido e acessível no próprio site.
* **Demonstrar Habilidades:** Servir como um projeto de portfólio robusto, evidenciando proficiência em Python, arquitetura de software, desenvolvimento web, CI/CD e boas práticas de engenharia.

## 4. Requisitos Funcionais

O chatbot DEVE:

* **RF1. Responder a Perguntas Frequentes (FAQ):**
    * **RF1.1. Base de Conhecimento Dinâmica:** O chatbot deve buscar respostas em uma base de dados de FAQs configurável.
    * **RF1.2. Reconhecimento de Palavras-Chave/Intenção:** Dada uma pergunta do usuário, o chatbot deve ser capaz de identificar a intenção ou palavras-chave para retornar a resposta mais relevante.
    * **RF1.3. Resposta Padrão:** Caso não entenda a pergunta, deve retornar uma mensagem padrão solicitando reformulação ou direcionando para outras opções de contato.
* **RF2. Coleta de Mensagens (Formulário Simplificado):**
    * **RF2.1. Iniciar Formulário:** O chatbot deve ser capaz de iniciar um fluxo para coleta de nome, e-mail e mensagem do usuário (opcionalmente, se a FAQ não for suficiente).
    * **RF2.2. Envio de Mensagem:** As mensagens coletadas devem ser armazenadas em um banco de dados e/ou enviadas para um e-mail pré-definido do Lab-Yes.
* **RF3. Interface de Usuário:**
    * **RF3.1. Widget Flutuante:** O chatbot deve ser um widget flutuante no canto inferior da tela do site.
    * **RF3.2. Histórico de Conversa:** Deve exibir o histórico da conversa na janela do chatbot.
    * **RF3.3. Campo de Entrada:** Deve ter um campo de texto para o usuário digitar mensagens e um botão de envio.
    * **RF3.4. Botão de Abrir/Fechar:** Deve ter um botão para abrir e fechar a janela do chatbot.
* **RF4. Gerenciamento de FAQs (Mínimo para MVP):**
    * **RF4.1. Adição de FAQs via API:** Deve haver um endpoint na API para adicionar novas FAQs (para uso inicial/teste manual).

## 5. Requisitos Não-Funcionais

* **RNF1. Performance:**
    * **RNF1.1. Tempo de Resposta:** As respostas do chatbot devem ser fornecidas em menos de 1 segundo para a maioria das requisições.
* **RNF2. Segurança:**
    * **RNF2.1. Proteção contra Injeção:** A aplicação deve ser protegida contra SQL Injection (garantido pelo uso de ORM).
    * **RNF2.2. Configuração de CORS:** O backend deve ter CORS configurado para permitir requisições apenas do domínio `lab-yes.com` (ou * para desenvolvimento).
    * **RNF2.3. Validação de Entrada:** Todas as entradas de usuário e da API devem ser validadas para prevenir dados maliciosos.
* **RNF3. Escalabilidade (Considerações para o Futuro):**
    * **RNF3.1. Preparado para Volume:** A arquitetura deve ser pensada para permitir uma futura migração para um banco de dados mais robusto (PostgreSQL) e para suportar um aumento no número de usuários.
    * **RNF3.2. Stateless (Backend):** O backend deve ser o máximo possível stateless para facilitar a escalabilidade horizontal.
* **RNF4. Manutenibilidade:**
    * **RNF4.1. Código Limpo:** O código deve seguir os padrões de linting e formatação (Black, Flake8).
    * **RNF4.2. Modularidade:** A lógica deve ser dividida em módulos e funções bem definidos.
    * **RNF4.3. Documentação Interna:** O código deve conter docstrings e comentários relevantes.
* **RNF5. Usabilidade:**
    * **RNF5.1. Intuitivo:** A interface do usuário deve ser simples e fácil de usar.
    * **RNF5.2. Acessibilidade (Básico):** Considerações básicas de contraste e tamanho de fonte.
* **RNF6. Confiabilidade:**
    * **RNF6.1. Tratamento de Erros:** A aplicação deve tratar erros de forma graciosa, sem travar ou expor detalhes internos.
    * **RNF6.2. Logging:** Mensagens de log relevantes devem ser geradas para monitoramento e depuração.
* **RNF7. Deploy & CI/CD:**
    * **RNF7.1. Conteinerização:** A aplicação deve ser conteinerizável com Docker.
    * **RNF7.2. Automação de Deploy:** Deve ser possível automatizar o deploy via GitHub Actions para uma plataforma de hospedagem (ex: Render.com).
    * **RNF7.3. Testes Automatizados:** Testes de unidade e integração devem ser executados automaticamente via CI.