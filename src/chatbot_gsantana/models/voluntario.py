from sqlalchemy import Column, Integer, String, JSON

# Removida a importação específica do dialeto PostgreSQL
# from sqlalchemy.dialects.postgresql import JSONB

from ..core.database import Base


class Voluntario(Base):
    """
    Modelo de dados para o perfil de um voluntário.
    """

    __tablename__ = "voluntarios"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, index=True)
    local = Column(String)
    hobbies = Column(String)

    # Alterado de JSONB para o tipo genérico JSON.
    # O SQLAlchemy irá usar JSONB no PostgreSQL e um fallback (TEXT) no SQLite.
    conhecimentos = Column(JSON)
