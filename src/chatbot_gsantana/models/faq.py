from sqlalchemy import Column, Integer, String

from ..core.database import Base


class FAQ(Base):
    """Modelo da tabela de Perguntas e Respostas Frequentes (FAQ)."""

    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True, nullable=False)
    answer = Column(String, nullable=False)
