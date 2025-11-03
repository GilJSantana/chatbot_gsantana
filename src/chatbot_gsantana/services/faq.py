import structlog
from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..repositories.faq import FaqRepository

logger = structlog.get_logger(__name__)


class FaqService:

    def __init__(self, repository: FaqRepository = Depends(), db: Session = Depends(get_db)):
        self.repository = repository
        self.db = db

    def get_answer_for_question(self, question_text: str) -> str | None:
        log = logger.bind(question=question_text)
        log.info("service.faq.get_answer.start")

        faq = self.repository.find_by_question_exact(self.db, question_text)
        
        if faq:
            log.info("service.faq.get_answer.found", faq_id=faq.id)
            return faq.answer
        else:
            log.info("service.faq.get_answer.not_found")
            return "Desculpe, não encontrei uma resposta para isso."
