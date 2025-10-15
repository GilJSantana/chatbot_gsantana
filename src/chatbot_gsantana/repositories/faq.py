from sqlalchemy.orm import Session

from ..models.faq import FAQ
from ..schemas.faq import FAQCreate, FAQUpdate


def create_faq(db: Session, faq: FAQCreate) -> FAQ:
    """Cria uma nova FAQ no banco de dados."""
    db_faq = FAQ(question=faq.question, answer=faq.answer)
    db.add(db_faq)
    db.flush()
    db.refresh(db_faq)
    return db_faq


def get_faq(db: Session, faq_id: int) -> FAQ | None:
    """Busca uma FAQ pelo seu ID."""
    return db.query(FAQ).filter(FAQ.id == faq_id).first()


def get_faqs(db: Session, skip: int = 0, limit: int = 100) -> list[FAQ]:
    """Busca todas as FAQs com paginação."""
    return db.query(FAQ).offset(skip).limit(limit).all()


def get_faq_by_question_text(db: Session, question_text: str) -> FAQ | None:
    """Busca uma FAQ pela pergunta exata."""
    return db.query(FAQ).filter(FAQ.question == question_text).first()


def update_faq(db: Session, faq_id: int, faq: FAQUpdate) -> FAQ | None:
    """Atualiza uma FAQ existente."""
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if db_faq:
        db_faq.question = faq.question
        db_faq.answer = faq.answer
        db.flush()
        db.refresh(db_faq)
    return db_faq


def delete_faq(db: Session, faq_id: int) -> FAQ | None:
    """Deleta uma FAQ existente."""
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if db_faq:
        db.delete(db_faq)
        db.flush()
    return db_faq
