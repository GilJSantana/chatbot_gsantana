# 1. Base Image
FROM python:3.13-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# 3. Install Poetry FIRST
RUN pip install poetry

# 4. Configure Poetry to create the venv inside the project
RUN poetry config virtualenvs.in-project true

# 5. Set Workdir
WORKDIR /app

# 6. Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# 7. Install dependencies (including dev dependencies for testing)
RUN poetry install --no-root --only main,dev

# 8. Add the venv to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# 9. Instala os navegadores do Playwright
RUN playwright install --with-deps

# 10. Copia todo o contexto do projeto para o diretório de trabalho
COPY . .

# 11. Torna o script de entrypoint executável
RUN chmod +x /app/entrypoint.sh

# 12. Define o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# 13. Expose port
EXPOSE 8000
