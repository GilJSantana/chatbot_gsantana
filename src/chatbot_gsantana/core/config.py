from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carrega as variáveis de ambiente para a aplicação."""

    DATABASE_URL: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
