# 1. Base Image
FROM python:3.13-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Workdir
WORKDIR /app

# 4. Install Poetry
RUN pip install poetry

# 5. Copy dependency files and install dependencies
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not create virtual envs and install
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --without dev

# 6. Copy application code
COPY ./src /app/src

# 7. Expose port and run server
EXPOSE 8000
CMD ["uvicorn", "src.chatbot_gsantana.main:app", "--host", "0.0.0.0", "--port", "8000"]
