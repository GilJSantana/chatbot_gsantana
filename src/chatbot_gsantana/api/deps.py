from collections.abc import Generator

from ..core.database import SessionLocal


def get_db() -> Generator:
    """Dependência para obter uma sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
