# 🛡️ Considerações de Segurança no Chatbot Gsantana

Este documento descreve as principais preocupações de segurança e as medidas de mitigação adotadas no projeto do Chatbot Gsantana. A segurança foi considerada desde o design da arquitetura para proteger o sistema e os dados dos usuários contra vulnerabilidades comuns.

## 1. Análise de Ameaças

A arquitetura do Chatbot Gsantana, conforme definida no [Modelo C4](02-modelo-c4.md), está exposta a algumas ameaças de segurança típicas para aplicações web e APIs. As principais áreas de preocupação incluem:

* **Injeção de Código Malicioso:** Riscos de injeção de SQL ou outros tipos de comandos via requisições da API.
* **Acesso Não Autorizado:** Tentativas de acesso aos endpoints de administração (`/api/faq/add`, etc.) por usuários não autorizados.
* **Validação de Dados de Entrada:** Entradas malformadas ou maliciosas que podem causar erros inesperados ou explorar vulnerabilidades.
* **Ataques de Negação de Serviço (DoS):** Tentativas de sobrecarregar a API com um grande volume de requisições.
* **Vulnerabilidades no Frontend:** Riscos como Cross-Site Scripting (XSS) se a saída da API for renderizada sem sanitização no navegador.

## 2. Medidas de Mitigação Implementadas

Para mitigar as ameaças identificadas, as seguintes práticas de segurança foram adotadas ou são consideradas na arquitetura do projeto:

### 2.1. Validação de Entrada e Proteção contra Injeção

* **Validação de Dados com Pydantic:** A API utiliza **FastAPI com modelos Pydantic** para definir schemas de dados rigorosos para todas as requisições. Isso garante que qualquer dado recebido pela API seja validado automaticamente. Se os dados não corresponderem aos tipos e formatos esperados, a requisição é rejeitada com um erro claro (422 Unprocessable Entity). Esta é a primeira e mais eficaz linha de defesa contra muitos tipos de ataques de injeção e dados maliciosos.
* **Uso de ORM:** A interação com o banco de dados é feita exclusivamente através do **SQLAlchemy ORM**. Isso garante que todas as consultas sejam parametrizadas, eliminando o risco de ataques de injeção de SQL.

### 2.2. Controle de Acesso e Autenticação

* **Endpoints de Administração Protegidos:** Os endpoints de administração (adição, edição, exclusão de FAQs) são a principal área de risco. A estratégia de segurança para eles é a implementação de um sistema de autenticação robusto.
* **Plano de Autenticação:** A solução planejada é o uso de **OAuth2 com Tokens JWT (JSON Web Token)**, um padrão moderno e seguro. O FastAPI possui suporte integrado para OAuth2, o que facilitará a implementação e garantirá que apenas usuários autenticados e autorizados possam acessar esses endpoints.

### 2.3. Segurança da Comunicação

* **Uso de HTTPS:** Em produção, a comunicação entre o frontend e a API deve sempre ser feita sobre **HTTPS** para criptografar os dados em trânsito, protegendo contra interceptação.
* **CORS (Cross-Origin Resource Sharing):** As configurações de CORS na API (via `CORSMiddleware` do FastAPI) serão estritas, permitindo requisições apenas de origens confiáveis (o domínio do Lab-Yes), para evitar que scripts maliciosos de outros sites acessem a API.

### 2.4. Logging e Monitoramento

* **Logging Estruturado:** O componente de logging registrará atividades importantes, incluindo requisições, erros e tentativas de acesso não autorizado. Adoção de logs estruturados (ex: JSON) para facilitar a análise por sistemas automatizados.
* **Monitoramento (Observabilidade):** Em um ambiente de produção, os logs, métricas e traces serão centralizados usando ferramentas como o stack ELK, Prometheus e Grafana para detectar comportamentos anômalos e tentativas de ataque em tempo real.

### 2.5. Proteção do Ambiente de Execução

* **Backend (API):**
    * **Modo Debug Desativado:** A aplicação em ambiente de produção **não deve** rodar com o modo debug do FastAPI/Uvicorn ativado, para evitar a exposição de informações sensíveis em caso de erro.
    * **Gerenciamento de Segredos:** Credenciais de banco de dados, chaves de API e outros segredos serão gerenciados através de **variáveis de ambiente** e carregados de forma segura pela aplicação (usando Pydantic-Settings), e não hardcoded no código.
* **Conteinerização:** O uso de **Docker** para conteinerizar a aplicação ajuda a isolar o ambiente de execução, reduzindo a superfície de ataque e garantindo consistência entre os ambientes.

## 3. Conclusão

As medidas de segurança adotadas, especialmente a validação automática de dados do FastAPI e o uso de ORM, criam uma base sólida. As próximas etapas críticas são a implementação da autenticação com OAuth2/JWT nos endpoints de administração e a configuração de um pipeline de deploy seguro com Docker e gerenciamento de segredos.

---