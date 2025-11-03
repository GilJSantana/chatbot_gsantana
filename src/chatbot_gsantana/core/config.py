import os
from functools import lru_cache
from typing import Optional, Union

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Carrega as variáveis de ambiente para a aplicação."""

    TEST_MODE: bool = False
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    DATABASE_URL: Optional[Union[PostgresDsn, str]] = None

    TEST_ADMIN_USERNAME: Optional[str] = None
    TEST_ADMIN_EMAIL: Optional[str] = None
    TEST_ADMIN_PASSWORD: Optional[str] = None

    def __init__(self, **values):
        super().__init__(**values)
        if not self.TEST_MODE and all([
            self.POSTGRES_SERVER,
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_DB
        ]):
            self.DATABASE_URL = str(PostgresDsn.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                path=f"{self.POSTGRES_DB}"  # CORREÇÃO: Sem a barra inicial
            ))
        elif self.TEST_MODE:
            self.DATABASE_URL = "sqlite:///:memory:"

    # A configuração do env_file é responsabilidade do Docker Compose
    model_config = SettingsConfigDict(case_sensitive=True)

@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instância cacheada das configurações."""
    return Settings()
