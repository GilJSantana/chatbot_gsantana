from sqlalchemy.orm import Session

from ..repositories.faq import FaqRepository


class FaqService:
    """
    Camada de serviço para a lógica de negócio relacionada a FAQs.
    """

    def __init__(self, repository: FaqRepository):
        self.repository = repository

    def get_answer_for_question(self, db: Session, question_text: str) -> str | None:
        """
        Busca a melhor resposta para uma dada pergunta.

        NOTA: A lógica atual é uma simulação simples. Uma implementação real
        usaria busca por similaridade de vetores (vector search) com embeddings
        de texto para encontrar a pergunta mais semanticamente similar.
        """
        faq = self.repository.find_by_question_exact(db, question_text)
        return faq.answer if faq else None


# Função de dependência para o FastAPI
def get_faq_service() -> FaqService:
    """
    Dependência do FastAPI que cria e fornece uma instância de FaqService.
    """
    repository = FaqRepository()
    return FaqService(repository=repository)
