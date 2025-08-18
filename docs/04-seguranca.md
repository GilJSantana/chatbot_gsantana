# 🛡️ Considerações de Segurança no Chatbot Gsantana

Este documento descreve as principais preocupações de segurança e as medidas de mitigação adotadas no projeto do Chatbot Gsantana. A segurança foi considerada desde o design da arquitetura para proteger o sistema e os dados dos usuários contra vulnerabilidades comuns.

## 1. Análise de Ameaças

A arquitetura do Chatbot Gsantana, conforme definida no [Modelo C4](02-modelo-c4.md), está exposta a algumas ameaças de segurança típicas para aplicações web e APIs. As principais áreas de preocupação incluem:

* **Injeção de Código Malicioso:** Riscos de injeção de SQL ou outros tipos de comandos via requisições da API, especialmente nos endpoints de administração.
* **Acesso Não Autorizado:** Tentativas de acesso aos endpoints de administração (`/add_faq`, `/edit_faq`, etc.) por usuários não autorizados.
* **Exposição de Dados Sensíveis:** Embora a API não lide com informações de identificação pessoal (PII), a exposição de dados de FAQs ou metadados do sistema pode ser um risco.
* **Ataques de Negação de Serviço (DoS):** Tentativas de sobrecarregar a API com um grande volume de requisições.
* **Vulnerabilidades no Frontend:** Riscos como Cross-Site Scripting (XSS) se a saída da API for renderizada sem sanitização no navegador.

## 2. Medidas de Mitigação Implementadas

Para mitigar as ameaças identificadas, as seguintes práticas de segurança foram adotadas ou são consideradas na arquitetura do projeto:

### 2.1. Proteção contra Injeção

* **Uso de ORM:** A interação com o banco de dados é feita exclusivamente através do **SQLAlchemy ORM**. Isso garante que todas as consultas sejam parametrizadas, prevenindo ataques de injeção de SQL.
* **Sanitização de Entrada:** O 'Validador de Entrada' (Input Validator) é responsável por validar e, quando necessário, sanitizar os dados recebidos em todos os endpoints da API.

### 2.2. Controle de Acesso e Autenticação

* **Endpoint de Administração:** O endpoint para gerenciar FAQs é a principal área de risco. No projeto atual, a segurança é baseada na confiança (ex: uso apenas em rede interna), mas um futuro aprimoramento seria a implementação de um sistema de autenticação.
* **Plano de Autenticação Futuro:** Um sistema robusto de autenticação, como **Token JWT (JSON Web Token)**, é a solução recomendada para proteger os endpoints de administração, garantindo que apenas usuários com um token válido e assinado possam acessá-los.

### 2.3. Segurança da Comunicação

* **Uso de HTTPS:** A comunicação entre o frontend e a API deve sempre ser feita sobre **HTTPS** para criptografar os dados em trânsito, protegendo contra interceptação de requisições e exposição de dados.
* **CORS (Cross-Origin Resource Sharing):** As configurações de CORS na API (via Flask-CORS) devem ser estritas, permitindo requisições apenas de origens confiáveis (por exemplo, o domínio do Lab-Yes), para evitar acesso indevido por scripts maliciosos de outros sites.

### 2.4. Logging e Monitoramento

* **Logging:** O 'Componente de Logging' registra atividades importantes, incluindo requisições de entrada, erros e potenciais tentativas de acesso não autorizado.
* **Monitoramento Futuro:** Em um ambiente de produção, os logs seriam centralizados e monitorados por ferramentas como ELK Stack (Elasticsearch, Logstash, Kibana) para detectar comportamentos anômalos e tentativas de ataque em tempo real.

### 2.5. Proteção de Componentes

* **Backend (API):**
    * **Desativação de Modo Debug:** A execução da aplicação em ambiente de produção **não deve** usar o modo debug do Flask, que pode expor informações sensíveis.
    * **Execução em WSGI:** O uso do Gunicorn para servir a aplicação é uma medida de segurança, pois ele é projetado para lidar com conexões HTTP e gerenciar processos de forma robusta, isolando a lógica de negócio do servidor web.
* **Frontend:**
    * **Sanitização de HTML/DOM:** Qualquer resposta de texto da API que possa conter HTML deve ser renderizada no frontend com cautela, usando bibliotecas de sanitização para evitar ataques de Cross-Site Scripting (XSS).

## 3. Conclusão

Embora o Chatbot Gsantana não lide com dados PII, a segurança foi uma consideração primordial. As medidas de mitigação implementadas (uso de ORM, sanitização de entrada, HTTPS) criam uma base sólida. As próximas etapas incluem a implementação de autenticação nos endpoints de administração e a adoção de práticas de monitoramento mais robustas para ambientes de produção.

---