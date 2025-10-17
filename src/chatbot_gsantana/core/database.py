from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from .config import settings # Importa as configurações

Base = declarative_base()

# CORREÇÃO: Inicializa o engine e a SessionLocal diretamente no carregamento do módulo
# Isso garante que eles estejam sempre disponíveis quando o módulo for importado.
engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependência do FastAPI que fornece uma sessão de banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependência anotada para injeção mais limpa nas rotas.
SessionDep = Annotated[Session, Depends(get_db)]
