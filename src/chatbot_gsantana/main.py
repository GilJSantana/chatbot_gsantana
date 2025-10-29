from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.api import api_router
from .core import database, logging_config
from .core.config import get_settings, Settings
from .api.middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida para inicializar e limpar recursos.
    """
    logging_config.configure_logging()

    # As configurações devem estar sempre disponíveis em app.state.settings
    settings = app.state.settings

    # Conecta ao banco de dados e armazena a fábrica de sessões no estado da aplicação
    session_factory = database.get_db_session_factory(str(settings.DATABASE_URL))
    app.state.db_session_factory = session_factory

    # A criação de tabelas deve ser gerenciada por uma ferramenta de migração (Alembic)
    # e não pela aplicação em tempo de execução. Comentando esta linha.
    engine = session_factory.kw["bind"]
    database.Base.metadata.create_all(bind=engine)

    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Fábrica de aplicação FastAPI.
    Se `settings` for fornecido, usa-o; caso contrário, carrega as configurações padrão.
    """
    app = FastAPI(
        title="Chatbot LabYes",
        description="API para o chatbot de FAQ do LabYes",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Armazena as configurações no estado da aplicação para acesso posterior
    app.state.settings = settings if settings else get_settings()

    app.add_middleware(LoggingMiddleware)

    origins = ["http://localhost", "http://localhost:80"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health-check")
    def health_check():
        return {"status": "ok"}

    return app


# Cria a aplicação principal para execução normal (não para testes)
app = create_app()
