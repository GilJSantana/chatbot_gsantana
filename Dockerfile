# Versão Python em que a aplicação foi desenvolvida
FROM python:3.13-slim as builder

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de gerenciamento de dependência do Poetry para o contêiner
# Isso otimiza o cache do Docker, pois essas linhas só rodam quando as dependências mudam
COPY pyproject.toml poetry.lock ./

# Instala o Poetry no contêiner
RUN pip install poetry

# Instala as dependências do projeto, excluindo as de desenvolvimento
# O --no-root evita que o poetry instale o próprio projeto como um pacote,
# o que será feito na próxima fase.
RUN poetry install --no-root --without dev

# 2. Fase Final (para o ambiente de execução)
# Usa uma nova imagem base mais leve para a execução
FROM python:3.13-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia as dependências instaladas da fase 'builder'
COPY --from=builder /app/.venv /app/.venv

# Configura o PATH para usar o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"

# Copia o restante do código da sua aplicação (o diretório 'backend/') para o contêiner
COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY docs/ ./docs/

# Expõe a porta que sua aplicação irá usar
EXPOSE 5000

# Comando para iniciar a aplicação com Gunicorn quando o contêiner for iniciado
# O --bind 0.0.0.0:5000 faz com que a API fique acessível de fora do contêiner
# Note que o comando agora aponta para o caminho correto do seu app: 'backend.app:app'
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "backend.app:app"]