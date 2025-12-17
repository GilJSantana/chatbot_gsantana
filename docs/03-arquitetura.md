# 📐 Decisões de Arquitetura do Chatbot Gsantana

Este documento detalha as principais decisões de arquitetura e os princípios que guiaram o desenvolvimento do Chatbot Gsantana. Ele serve como um complemento aos [diagramas do Modelo C4](02-modelo-c4.md), explicando o raciocínio por trás das escolhas tecnológicas e estruturais.

## 1. Princípios de Design

O projeto Chatbot Gsantana foi guiado pelos seguintes princípios de design:

* **Simplicidade e Clareza:** Optar por soluções diretas e compreensíveis, evitando complexidade desnecessária.
* **Modularidade:** Dividir o sistema em componentes e módulos coesos e de baixo acoplamento para facilitar a manutenção e evolução.
* **Escalabilidade (Inicial e Futura):** Desenvolver uma base que permita o crescimento futuro, mesmo que a solução inicial seja mais simples.
* **Testabilidade:** Projetar componentes de forma que possam ser testados isoladamente e integrados com confiança.
* **Confiabilidade:** Garantir que o chatbot seja robusto e capaz de lidar com requisições de forma consistente.
* **Manutenibilidade:** Facilitar a compreensão e as modificações futuras no código.

## 2. Visão Geral da Arquitetura

O Chatbot Gsantana segue uma arquitetura de microsserviço para a API principal, complementada por um frontend desacoplado. A comunicação é RESTful.

* **Backend (API do Chatbot):** Responsável pela lógica de negócio principal, gerenciamento de FAQs e integração com o banco de dados.
* **Frontend (Aplicação no Navegador):** Interface do usuário que interage com a API e exibe as respostas do chatbot.
* **Banco de Dados:** Armazenamento persistente para as perguntas e respostas frequentes.

## 3. Decisões Tecnológicas Chave

### 3.1. Linguagem e Framework do Backend: Python com FastAPI

* **Porquê Python:**
    * **Produtividade:** Sintaxe clara e vasta gama de bibliotecas.
    * **Comunidade:** Grande comunidade e ecossistema robusto para IA, processamento de dados e web.
* **Porquê FastAPI:**
    * **Alta Performance:** Sendo um dos frameworks Python mais rápidos disponíveis, o FastAPI nos ajuda a cumprir o requisito de tempo de resposta (RNF1.1) de forma mais eficaz que alternativas como o Flask.
    * **Validação de Dados Nativa:** Utiliza Pydantic para validar automaticamente os dados de entrada e saída, o que reduz a quantidade de código boilerplate e aumenta a segurança e a robustez da API.
    * **Documentação Automática:** Gera documentação interativa da API (Swagger UI e ReDoc) automaticamente a partir do código, garantindo que a documentação esteja sempre atualizada e facilitando os testes.
    * **Moderno e Assíncrono:** Construído sobre ASGI (Asynchronous Server Gateway Interface), o que o torna ideal para aplicações com alta concorrência e operações de I/O, como chamadas a bancos de dados e outras APIs.
    * **Ecossistema Rico:** Inclui suporte para injeção de dependências e ferramentas que facilitam a criação de interfaces de administração, como a utilizada neste projeto.

### 3.2. Gerenciamento de Dependências: Poetry

* **Porquê Poetry:**
    * **Gerenciamento de Dependências Determinístico:** Garante que builds sejam reproduzíveis.
    * **Ambientes Virtuais Integrados:** Facilita a criação e gerenciamento de ambientes isolados.
    * **Ferramenta All-in-One:** Simplifica o fluxo de trabalho de desenvolvimento.

### 3.3. Banco de Dados: SQLite (testes) e PostgreSQL (Produção)

* **Porquê SQLite (para testes):**
    * **Simplicidade:** Banco de dados em arquivo único, ideal para prototipagem e testes locais.
    * **Facilidade de Setup:** Não requer um servidor de banco de dados separado.
* **Porquê PostgreSQL (para produção):**
    * **Robustez e Escalabilidade:** Um sistema de banco de dados relacional completo, capaz de lidar com um volume maior de dados e acessos concorrentes.
    * **Recursos Avançados:** Suporte a tipos de dados complexos, transações e confiabilidade, essencial para um ambiente de produção.

### 3.4. Servidor ASGI: Uvicorn

* **Porquê Uvicorn:**
    * **Servidor ASGI de Alta Performance:** É o servidor recomendado para aplicações FastAPI, construído para lidar com a natureza assíncrona do framework.
    * **Leve e Rápido:** Garante que a aplicação seja servida com o mínimo de sobrecarga.

### 3.5. Frontend: JavaScript/HTML/CSS

* **Porquê Web Technologies Puras:**
    * **Flexibilidade e Leveza:** Permite criar uma interface minimalista sem a sobrecarga de grandes frameworks.
    * **Fácil Integração:** A interface pode ser incorporada em qualquer página web existente.

## 4. Padrões de Design Aplicados (na API do Chatbot)

* **Arquitetura em Camadas:** Separação clara entre a camada de apresentação (rotas/routers), lógica de negócio (serviços) e acesso a dados (repositórios).
* **Padrão Repositório:** Abstração da camada de persistência (`FAQRepository`), isolando a lógica de acesso ao banco de dados.
* **Injeção de Dependências:** O FastAPI facilita a injeção de dependências (como sessões de banco de dados ou serviços) nos endpoints da API, melhorando a testabilidade.
* **Validação com Pydantic:** Uso de modelos Pydantic para definir schemas de dados claros, garantindo a validação e a serialização de forma automática.

## 5. Próximos Passos e Evolução

* **Cache:** Introdução de Redis para cachear as FAQs mais acessadas, melhorando a performance.
* **Autenticação e Autorização:** Implementação de JWT ou OAuth2 (recursos já suportados pelo FastAPI) para proteger endpoints de administração.
* **Observabilidade:** Integração com ferramentas de logging, métricas e tracing (ex: ELK Stack, Prometheus, Grafana) para monitorar a saúde da aplicação em produção.
* **Conteinerização e CI/CD:** A estratégia principal de deploy será baseada em Docker e GitHub Actions para automação completa.

---