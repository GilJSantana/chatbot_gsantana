import secrets
from typing import Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carrega as variáveis de ambiente para a aplicação."""

    # --- Configurações da API ---
    API_V1_STR: str = "/api/v1"

    # --- Configurações de Segurança ---
    # CORREÇÃO: A chave secreta agora deve ser carregada do ambiente.
    # Não deve ser gerada dinamicamente.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Configurações do Banco de Dados (PostgreSQL) ---
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    # --- URL do Banco de Dados ---
    # Pode ser definida diretamente ou construída a partir das variáveis do Postgres.
    # O padrão é um banco SQLite para desenvolvimento local e testes.
    DATABASE_URL: Union[str, None] = "sqlite:///./test_db.db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
