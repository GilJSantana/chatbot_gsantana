from functools import lru_cache
from typing import Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carrega as variáveis de ambiente para a aplicação."""

    # --- Configurações da API ---
    API_V1_STR: str = "/api/v1"

    # --- Configurações de Segurança ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Configurações do Banco de Dados (PostgreSQL) ---
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    # --- URL do Banco de Dados ---
    DATABASE_URL: Union[str, None] = "sqlite:///./test_db.db"

    # Por padrão, Pydantic's BaseSettings irá carregar variáveis de um arquivo .env
    # se python-dotenv estiver instalado. Para testes, pytest-dotenv irá carregar o
    # arquivo .env.test especificado no ambiente, e as variáveis de ambiente
    # têm maior prioridade do que os valores de um arquivo .env.
    model_config = SettingsConfigDict(case_sensitive=True)


@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instância cacheada das configurações."""
    return Settings()
