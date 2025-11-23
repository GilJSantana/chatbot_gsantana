from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine

from .api.v1.api import api_router
from .core import database, logging_config
from .core.config import get_settings
from .api.middleware import LoggingMiddleware
from .core.database import Base

# Engine global para ser usado com SQLite em memória
engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida para inicializar e limpar recursos.
    """
    global engine
    logging_config.configure_logging()

    settings = get_settings()

    if settings.TEST_MODE:
        if engine is None:
            engine = create_engine(
                str(settings.DATABASE_URL), connect_args={"check_same_thread": False}
            )
        session_factory = database.get_db_session_factory(existing_engine=engine)
        Base.metadata.create_all(bind=engine)
    else:
        session_factory = database.get_db_session_factory(str(settings.DATABASE_URL))
        engine = session_factory.kw["bind"]
        Base.metadata.create_all(bind=engine)

    app.state.db_session_factory = session_factory

    # A lógica de criação automática do admin foi removida.
    # A criação de administradores agora é feita exclusivamente
    # através do script 'manage.py'.

    yield


def create_app() -> FastAPI:
    """
    Fábrica de aplicação FastAPI.
    """
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


app = create_app()
