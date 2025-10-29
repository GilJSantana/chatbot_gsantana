from sqlalchemy.orm import Session

from ..models.faq import FAQ
from ..schemas.faq import FAQCreate, FAQUpdate


class FaqRepository:
    """
    Encapsula a lógica de acesso a dados para o modelo FAQ.
    """

    def create_faq(self, db: Session, faq: FAQCreate) -> FAQ:
        db_faq = FAQ(question=faq.question, answer=faq.answer)
        db.add(db_faq)
        db.flush()
        db.refresh(db_faq)
        return db_faq

    def get_faq(self, db: Session, faq_id: int) -> FAQ | None:
        return db.query(FAQ).filter(FAQ.id == faq_id).first()

    def get_faqs(self, db: Session, skip: int = 0, limit: int = 100) -> list[FAQ]:
        return db.query(FAQ).offset(skip).limit(limit).all()

    def find_by_question_exact(self, db: Session, question_text: str) -> FAQ | None:
        """Busca uma FAQ pela pergunta exata (case-insensitive)."""
        # A implementação de case-insensitive pode variar com o DB,
        # aqui usamos lower() que funciona bem em PostgreSQL e SQLite.
        return db.query(FAQ).filter(FAQ.question.ilike(f"%{question_text}%")).first()

    def update_faq(self, db: Session, faq_id: int, faq: FAQUpdate) -> FAQ | None:
        db_faq = self.get_faq(db, faq_id)
        if db_faq:
            db_faq.question = faq.question
            db_faq.answer = faq.answer
            db.flush()
            db.refresh(db_faq)
        return db_faq

    def delete_faq(self, db: Session, faq_id: int) -> FAQ | None:
        db_faq = self.get_faq(db, faq_id)
        if db_faq:
            db.delete(db_faq)
            db.flush()
        return db_faq


# Instância singleton para ser usada por padrão, mas permitindo override.
faq_repository = FaqRepository()
