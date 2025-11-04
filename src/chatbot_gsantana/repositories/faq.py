from sqlalchemy.orm import Session

from ..models.faq import FAQ
from ..schemas.faq import FAQCreate, FAQUpdate


class FaqRepository:

    def create_faq(self, db: Session, faq: FAQCreate) -> FAQ:
        db_faq = FAQ(question=faq.question, answer=faq.answer)
        db.add(db_faq)
        db.commit()
        db.refresh(db_faq)
        return db_faq

    def get_faq(self, db: Session, faq_id: int) -> FAQ | None:
        return db.query(FAQ).filter(FAQ.id == faq_id).first()

    def get_faqs(self, db: Session, skip: int = 0, limit: int = 100) -> list[FAQ]:
        return db.query(FAQ).offset(skip).limit(limit).all()

    def find_by_question_exact(self, db: Session, question_text: str) -> FAQ | None:
        return db.query(FAQ).filter(FAQ.question.ilike(question_text)).first()

    def find_by_question(self, db: Session, question_text: str) -> FAQ | None:
        return db.query(FAQ).filter(FAQ.question.ilike(f"%{question_text}%")).first()

    def update_faq(self, db: Session, faq_id: int, faq: FAQUpdate) -> FAQ | None:
        db_faq = self.get_faq(db, faq_id)
        if db_faq:
            db_faq.question = faq.question
            db_faq.answer = faq.answer
            db.commit()
            db.refresh(db_faq)
        return db_faq

    def delete_faq(self, db: Session, faq_id: int) -> FAQ | None:
        db_faq = self.get_faq(db, faq_id)
        if db_faq:
            db.delete(db_faq)
            db.commit()
        return db_faq

    def delete_faq_by_question(self, db: Session, question: str) -> FAQ | None:
        db_faq = self.find_by_question_exact(db, question)
        if db_faq:
            db.delete(db_faq)
            db.commit()
        return db_faq
