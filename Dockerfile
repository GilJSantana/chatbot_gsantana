# Stage 1: Builder - A "fat" image with all code and dependencies for testing
FROM python:3.13-slim as builder

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# Add PYTHONPATH to ensure scripts can find the application module
ENV PYTHONPATH=/app/src

# Install Poetry
RUN pip install poetry

# Set Workdir
WORKDIR /app

# Copy dependency files and install all dependencies (including dev)
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

# Set the PATH to use the virtual environment, so we can use the 'playwright' command
ENV PATH="/app/.venv/bin:$PATH"

# Install Playwright browsers and their system dependencies
RUN playwright install --with-deps

# Copy all the application code, including tests
COPY . .


# Stage 2: Production - The final lean image for deployment
FROM python:3.13-slim as production

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Set Workdir
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv

# Copy only the necessary application source code from the builder stage
COPY --from=builder /app/src ./src
COPY --from=builder /app/html ./html
COPY --from=builder /app/entrypoint.sh ./
COPY --from=builder /app/manage.py ./

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the PATH to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose the application port
EXPOSE 8000

# Define the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
