from backend.app import db
from backend.models import FAQ
from sqlalchemy import or_

class FAQRepository:
    def get_all_faqs(self):
        return FAQ.query.all()

    def get_faq_by_id(self, faq_id):
        return FAQ.query.get(faq_id)

    def search_faqs(self, query:str):
        search_term = f'%{query.lower()}%'
        return FAQ.query.filter(
            or_(
                db.func.lower(FAQ.question).like(search_term),
                db.func.lower(FAQ.answer).like(search_term)
            )
        ).all()

    def add_faq(self, question, answer):
        new_faq = FAQ(question=question,answer=answer)
        db.session.add(new_faq)
        db.session.commit()
        return new_faq

    def update_faq(self, faq_id, new_question, new_answer):
        faq = self.get_faq_by_id(faq_id)
        if faq:
            faq.question = new_question
            faq.answer = new_answer
            db.session.commit()
            return faq
        return None

    def delete_faq(self, faq_id):
        faq = self.get_faq_by_id(faq_id)
        if faq:
            db.session.delete(faq)
            db.session.commit()
            return True
        return False
