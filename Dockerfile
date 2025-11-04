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

# 9. CORREÇÃO: Instala as dependências do sistema e os navegadores com o comando oficial do Playwright
RUN playwright install --with-deps

# 10. Copy application code
COPY ./src /app/src
COPY ./scripts /app/scripts
COPY ./tests /app/tests
COPY pytest.ini /app/pytest.ini

# 11. Expose port
EXPOSE 8000

# O CMD foi removido, pois o comando será definido no docker-compose.yml
