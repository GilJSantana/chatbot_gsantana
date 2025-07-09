# 📐 Decisões de Arquitetura do Chatbot Lab-Yes

Este documento detalha as principais decisões de arquitetura e os princípios que guiaram o desenvolvimento do Chatbot Lab-Yes. Ele serve como um complemento aos [diagramas do Modelo C4](02-modelo-c4.md), explicando o raciocínio por trás das escolhas tecnológicas e estruturais.

## 1. Princípios de Design

O projeto Chatbot Lab-Yes foi guiado pelos seguintes princípios de design:

* **Simplicidade e Clareza:** Optar por soluções diretas e compreensíveis, evitando complexidade desnecessária.
* **Modularidade:** Dividir o sistema em componentes e módulos coesos e de baixo acoplamento para facilitar a manutenção e evolução.
* **Escalabilidade (Inicial e Futura):** Desenvolver uma base que permita o crescimento futuro, mesmo que a solução inicial seja mais simples.
* **Testabilidade:** Projetar componentes de forma que possam ser testados isoladamente e integrados com confiança.
* **Confiabilidade:** Garantir que o chatbot seja robusto e capaz de lidar com requisições de forma consistente.
* **Manutenibilidade:** Facilitar a compreensão e as modificações futuras no código.

## 2. Visão Geral da Arquitetura

O Chatbot Lab-Yes segue uma arquitetura baseada em **microsserviços para a API principal**, complementada por um frontend desacoplado. A comunicação é majoritariamente RESTful.

* **Backend (API do Chatbot):** Responsável pela lógica de negócio principal, gerenciamento de FAQs e integração com o banco de dados.
* **Frontend (Aplicação no Navegador):** Interface do usuário que interage com a API e exibe as respostas do chatbot.
* **Banco de Dados:** Armazenamento persistente para as perguntas e respostas frequentes.

## 3. Decisões Tecnológicas Chave

### 3.1. Linguagem e Framework do Backend: Python com Flask

* **Porquê Python:**
    * **Produtividade:** Sintaxe clara e vasta gama de bibliotecas.
    * **Comunidade:** Grande comunidade e ecossistema robusto.
    * **Facilidade de Prototipagem e Desenvolvimento Rápido:** Ideal para a fase inicial do projeto.
* **Porquê Flask:**
    * **Micro-framework:** Leve e flexível, permitindo construir apenas o que é necessário.
    * **Controle Total:** Dá ao desenvolvedor mais controle sobre a escolha de bibliotecas e componentes.
    * **Desempenho (com Gunicorn):** Embora seja um micro-framework, combinado com Gunicorn (servidor WSGI), oferece bom desempenho e concorrência para casos de uso de APIs.

### 3.2. Gerenciamento de Dependências: Poetry

* **Porquê Poetry:**
    * **Gerenciamento de Dependências Determinístico:** Garante que builds sejam reproduzíveis.
    * **Ambientes Virtuais Integrados:** Facilita a criação e gerenciamento de ambientes isolados.
    * **Publicação de Pacotes:** Prepara o terreno caso a API precise ser empacotada.
    * **Ferramenta All-in-One:** Simplifica o fluxo de trabalho de desenvolvimento.

### 3.3. Banco de Dados: SQLite

* **Porquê SQLite:**
    * **Simplicidade:** Banco de dados em arquivo único, ideal para aplicações menores e prototipagem.
    * **Facilidade de Setup:** Não requer um servidor de banco de dados separado, o que simplifica o ambiente de desenvolvimento.
    * **Portabilidade:** O arquivo do banco de dados pode ser facilmente movido.
    * **Escalabilidade Futura:** Entende-se que para maior escalabilidade e concorrência, uma solução como PostgreSQL ou MySQL seria mais adequada, mas para a necessidade atual, o SQLite é suficiente.

### 3.4. Servidor WSGI: Gunicorn

* **Porquê Gunicorn:**
    * **Servidor Python Robusto:** Amplamente utilizado em produção para servir aplicações WSGI (como Flask).
    * **Concorrência:** Gerencia múltiplos workers, permitindo que a API lide com várias requisições simultaneamente de forma eficiente.
    * **Simplicidade de Configuração:** Fácil de integrar e configurar com aplicações Flask.

### 3.5. Frontend: JavaScript/HTML/CSS

* **Porquê Web Technologies Puras:**
    * **Flexibilidade e Leveza:** Permite criar uma interface minimalista e customizável sem a sobrecarga de grandes frameworks (como React, Angular, Vue) para este caso de uso simples.
    * **Fácil Integração:** A interface pode ser incorporada em qualquer página web existente com poucas linhas de código.
    * **Foco na Interação via API:** Reforça a natureza da API como o core do sistema.

## 4. Padrões de Design Aplicados (na API do Chatbot)

Dentro da API do Chatbot, foram aplicados alguns padrões de design para promover a modularidade e a testabilidade:

* **Arquitetura em Camadas (Implicitamente):** Separação clara entre a camada de apresentação (rotas), lógica de negócio (serviços) e acesso a dados (repositórios).
* **Padrão Repositório:** Abstração da camada de persistência (`FAQRepository`), isolando a lógica de acesso ao banco de dados do restante da aplicação. Isso facilita a troca do banco de dados no futuro sem impactar as camadas superiores.
* **Injeção de Dependências (Implicita/Manual):** Componentes como o `FAQService` podem receber o `FAQRepository` como dependência, facilitando testes unitários com mocks.
* **Validação de Entrada:** Módulo dedicado para validar os dados recebidos, garantindo a integridade e segurança.

## 5. Próximos Passos e Evolução (Considerações Futuras)

Embora o design atual atenda aos requisitos, futuras melhorias e expansões podem incluir:

* **Migração de Banco de Dados:** Para PostgreSQL ou MySQL para maior escalabilidade e recursos de concorrência.
* **Autenticação e Autorização:** Implementação de JWT ou OAuth para proteger endpoints de administração.
* **Cache:** Introdução de camadas de cache (ex: Redis) para FAQs muito acessadas.
* **Integração com LLMs:** Conectar o chatbot a modelos de linguagem grandes para respostas mais dinâmicas e contextuais.
* **Contêineres e Orquestração:** Utilização de Docker e Kubernetes para implantação e gerenciamento de microsserviços em produção.
* **CI/CD:** Implementação de pipelines de Integração Contínua e Entrega Contínua para automatizar testes e implantações.

---