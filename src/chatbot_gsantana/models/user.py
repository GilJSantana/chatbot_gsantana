from sqlalchemy import Column, Integer, String

from ..core.database import Base


class User(Base):
    """Modelo de dados para o usuário administrador."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
