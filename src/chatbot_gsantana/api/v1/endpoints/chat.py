from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....schemas.faq import Question, Answer # CORREÇÃO: Importa Question e Answer diretamente
from ....api import deps
from ....services.faq import faq_service

router = APIRouter()


@router.post("/", response_model=Answer) # Usa Answer diretamente
def ask_question(question: Question, db: Session = Depends(deps.get_db)):
    """
    Recebe uma pergunta do usuário e retorna a melhor resposta encontrada.
    """
    # A lógica de busca será implementada no faq_service em breve.
    answer = faq_service.get_answer_for_question(db=db, question_text=question.question)

    if not answer:
        # Se nenhuma resposta for encontrada, retorna uma mensagem padrão.
        return Answer(
            answer="Desculpe, não encontrei uma resposta para essa pergunta. Tente reformular."
        )

    return Answer(answer=answer)
