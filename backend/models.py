from .database import db


class FAQ(db.Model):
    __tablename__ = 'faq'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<FAQ {self.id} - "{self.question[:30]}...">'

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }
