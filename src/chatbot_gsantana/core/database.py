from typing import Annotated, Generator, Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import (
    sessionmaker,
    Session,
    declarative_base,
)  # Importa declarative_base do lugar certo
from fastapi import Depends, Request  # Importa Request

# Base para os modelos declarativos do SQLAlchemy
Base = declarative_base()


def get_db_session_factory(
    database_url: Optional[str] = None, existing_engine: Optional[Engine] = None
):
    """
    Retorna uma fábrica de sessões do SQLAlchemy.
    Se um existing_engine for fornecido,
    usa-o. Caso contrário, cria um novo com a database_url.
    """
    if existing_engine is None:
        if database_url is None:
            raise ValueError("Either database_url or existing_engine must be provided.")
        engine = create_engine(database_url, pool_pre_ping=True)
    else:
        engine = existing_engine

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def get_db(request: Request) -> Generator[Session, None, None]:  # Injeta Request
    """
    Dependência para obter uma sessão de banco de dados.
    """
    session_factory = request.app.state.db_session_factory
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
