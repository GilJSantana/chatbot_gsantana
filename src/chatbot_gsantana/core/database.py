from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

Base = declarative_base()


# As variáveis globais foram removidas para evitar
# condições de corrida na inicialização.
# engine = None
# SessionLocal = None


def get_db_session_factory(db_url: str) -> sessionmaker:
    """Cria e retorna uma fábrica de sessões para a URL do banco de dados fornecida."""
    engine = create_engine(db_url, pool_pre_ping=True)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(request: Request) -> Generator[Session, None, None]:
    """
    Dependência do FastAPI que fornece uma
    sessão de banco de dados a partir do estado da aplicação.
    """
    session_factory = getattr(request.app.state, "db_session_factory", None)
    if session_factory is None:
        raise RuntimeError(
            "Fábrica de sessão de banco de dados não encontrada no estado da aplicação."
        )

    db = session_factory()
    try:
        yield db
    finally:
        db.close()


# Dependência anotada para injeção mais limpa nas rotas.
SessionDep = Annotated[Session, Depends(get_db)]
