from sqlalchemy.orm import Session

from .. import models, schemas
from ..repositories import faq as faq_repository


class FAQService:
    """Camada de serviço para a lógica de negócio das FAQs."""

    def create_faq(self, db: Session, faq: schemas.FAQCreate) -> models.FAQ:
        """Cria uma nova FAQ."""
        return faq_repository.create_faq(db=db, faq=faq)

    def get_faq(self, db: Session, faq_id: int) -> models.FAQ | None:
        """Busca uma FAQ pelo ID."""
        return faq_repository.get_faq(db=db, faq_id=faq_id)

    def get_faqs(self, db: Session, skip: int = 0, limit: int = 100) -> list[models.FAQ]:
        """Busca todas as FAQs."""
        return faq_repository.get_faqs(db=db, skip=skip, limit=limit)

    def update_faq(self, db: Session, faq_id: int, faq: schemas.FAQCreate) -> models.FAQ | None:
        """Atualiza uma FAQ."""
        return faq_repository.update_faq(db=db, faq_id=faq_id, faq=faq)

    def delete_faq(self, db: Session, faq_id: int) -> models.FAQ | None:
        """Deleta uma FAQ."""
        return faq_repository.delete_faq(db=db, faq_id=faq_id)


faq_service = FAQService()
