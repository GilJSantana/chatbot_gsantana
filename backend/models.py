from backend.app import db

class FAQ(db.Model):
    __tablename__= 'faq'
    id = db.Columm(db.Integer, primary_key=True)
    question = db.Columm(db.String(255),nullable=False)
    answer = db.Columm(db.Text, nullable=False)

    def __repr__(self):
        return f'<FAQ {self.id} - "{self.question[:30]}...">'

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }