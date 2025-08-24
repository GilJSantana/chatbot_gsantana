from backend.repositories.faq_repository import FAQRepository

class FAQServices:
    def __init__(self, faq_repository: FAQRepository):
        self.faq_repository = faq_repository

    def get_all_faqs(self):
        return self.faq_repository.get_all_faqs()

    def get_faq_by_id(self,fad_id):
        return self.faq_repository.get_faq_by_id(fad_id)

    def search_faqs(self, query):
        if not query:
            return []
        return self.faq_repository.search_faqs(query)

    def add_faq(self, data):
        question = data.get('question')
        answer = data.get('answer')
        if not question or not answer:
            raise ValueError('Pergunta e reposta são obrigatórias.')
        return self.faq_repository.add_faq(question, answer)

    def update_faq(self, faq_id, data):
        question = data.get('question')
        answer = data.get('answer')
        if not question or not answer:
            raise ValueError('Perguta e reposta são obrigatórias.')
        return self.faq_repository.update_faq(faq_id,question, answer)

    def delete_faq(self, faq_id):
        return self.faq_repository.delete_faq(faq_id)