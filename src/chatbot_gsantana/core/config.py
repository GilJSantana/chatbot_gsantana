import secrets
from typing import Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carrega as variáveis de ambiente para a aplicação."""

    # --- Configurações de Segurança ---
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Configurações do Banco de Dados ---
    # Em produção (Docker), estes valores são lidos do .env.
    # Para testes (CI/CD), eles serão None, e a DATABASE_URL usará o SQLite.
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Constrói a URL de conexão com o banco de dados."""
        if self.POSTGRES_USER and self.POSTGRES_PASSWORD and self.POSTGRES_DB:
            return (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_SERVER or 'db'}/{self.POSTGRES_DB}"
            )
        # Retorna um banco de dados SQLite em memória para o ambiente de teste
        return "sqlite:///./test_db.db"

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
