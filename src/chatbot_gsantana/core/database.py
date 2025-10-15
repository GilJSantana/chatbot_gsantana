from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()

# As variáveis do engine e da sessão são inicializadas como None.
# Elas serão configuradas pela função `initialize_database`.
engine = None
SessionLocal = None


def initialize_database(database_url: str, **kwargs):
    """Inicializa o engine e a SessionLocal com a URL do banco de dados."""
    global engine, SessionLocal
    engine = create_engine(database_url, pool_pre_ping=True, **kwargs)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependência do FastAPI que fornece uma sessão de banco de dados.
    Levanta um erro se o banco de dados não for inicializado primeiro.
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Database not initialized. Call initialize_database() first."
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependência anotada para injeção mais limpa nas rotas.
SessionDep = Annotated[Session, Depends(get_db)]
