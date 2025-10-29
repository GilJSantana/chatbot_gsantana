import structlog
from sqlalchemy.orm import Session

from ..repositories.faq import FaqRepository

logger = structlog.get_logger(__name__)


class FaqService:
    """
    Camada de serviço para a lógica de negócio relacionada a FAQs.
    """

    def __init__(self, repository: FaqRepository):
        self.repository = repository

    def get_answer_for_question(self, db: Session, question_text: str) -> str | None:
        """
        Busca a melhor resposta para uma dada pergunta.
        """
        log = logger.bind(question=question_text)
        log.info("service.faq.get_answer.start")

        faq = self.repository.find_by_question_exact(db, question_text)
        
        if faq:
            log.info("service.faq.get_answer.found", faq_id=faq.id)
            return faq.answer
        else:
            log.info("service.faq.get_answer.not_found")
            return None


# Função de dependência para o FastAPI
def get_faq_service() -> FaqService:
    """
    Dependência do FastAPI que cria e fornece uma instância de FaqService.
    """
    repository = FaqRepository()
    return FaqService(repository=repository)
