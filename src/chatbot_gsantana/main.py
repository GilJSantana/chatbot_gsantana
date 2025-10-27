from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.api import api_router
from .core import database, logging_config
from .core.config import get_settings
from .api.middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida para inicializar e limpar recursos.
    """
    logging_config.configure_logging()

    settings = get_settings()
    # Conecta ao banco de dados e armazena a fábrica de sessões no estado da aplicação
    app.state.db_session_factory = database.get_db_session_factory(
        str(settings.DATABASE_URL)
    )

    # Opcional: Cria as tabelas se não estiver usando migrações como Alembic
    # database.Base.metadata.create_all(bind=app.state.db_session_factory.kw["bind"])

    yield

    # Opcional: Limpa recursos ao desligar
    # if hasattr(app.state, "db_session_factory"):
    #     engine = app.state.db_session_factory.kw["bind"]
    #     engine.dispose()


def create_app() -> FastAPI:
    """Fábrica de aplicação FastAPI."""
    app = FastAPI(
        title="Chatbot LabYes",
        description="API para o chatbot de FAQ do LabYes",
        version="0.1.0",
        lifespan=lifespan,
    )

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
