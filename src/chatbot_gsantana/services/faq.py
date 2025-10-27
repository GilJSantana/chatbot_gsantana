from __future__ import annotations
import structlog
from sqlalchemy.orm import Session

from .. import models, schemas
from ..repositories import faq as faq_repository

log = structlog.get_logger()


class FAQService:
    """Camada de serviço para a lógica de negócio das FAQs."""

    def create_faq(self, db: Session, faq: schemas.FAQCreate) -> models.FAQ:
        """Cria uma nova FAQ e confirma a transação."""
        db_faq = faq_repository.create_faq(db=db, faq=faq)
        db.commit()
        db.refresh(db_faq)
        log.info("faq_created", faq_id=db_faq.id, question=db_faq.question)
        return db_faq

    def get_faq(self, db: Session, faq_id: int) -> models.FAQ | None:
        """Busca uma FAQ pelo ID."""
        return faq_repository.get_faq(db=db, faq_id=faq_id)

    def get_faqs(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[models.FAQ]:
        """Busca todas as FAQs."""
        return faq_repository.get_faqs(db=db, skip=skip, limit=limit)

    def update_faq(
        self, db: Session, faq_id: int, faq: schemas.FAQUpdate
    ) -> models.FAQ | None:
        """Atualiza uma FAQ e confirma a transação se encontrada."""
        db_faq = faq_repository.update_faq(db=db, faq_id=faq_id, faq=faq)
        if db_faq:
            db.commit()
            db.refresh(db_faq)
            log.info("faq_updated", faq_id=db_faq.id)
        return db_faq

    def delete_faq(self, db: Session, faq_id: int) -> bool:
        """Deleta uma FAQ e confirma a transação, retornando True se bem-sucedido."""
        deleted_faq = faq_repository.delete_faq(db=db, faq_id=faq_id)
        if deleted_faq:
            db.commit()
            log.info("faq_deleted", faq_id=faq_id)
            return True
        return False

    def get_answer_for_question(self, db: Session, question_text: str) -> str | None:
        """Busca a resposta para uma pergunta, por correspondência exata."""
        faq = faq_repository.get_faq_by_question_text(
            db=db, question_text=question_text
        )
        if faq:
            return faq.answer
        return None


faq_service = FAQService()
