from fastapi import APIRouter, status, HTTPException, Depends

from chatbot_gsantana import schemas
from chatbot_gsantana.api import deps
from chatbot_gsantana.services.faq import FaqService

router = APIRouter()


@router.get("/", response_model=list[schemas.FAQ])
def get_faqs(
    faq_service: FaqService = Depends(),
    skip: int = 0,
    limit: int = 100,
):
    return faq_service.repository.get_faqs(faq_service.db, skip=skip, limit=limit)


@router.get("/{faq_id}", response_model=schemas.FAQ)
def get_faq(faq_id: int, faq_service: FaqService = Depends()):
    db_faq = faq_service.repository.get_faq(faq_service.db, faq_id=faq_id)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq


@router.post(
    "/",
    response_model=schemas.FAQ,
    status_code=status.HTTP_201_CREATED,
)
def create_faq(
    faq_in: schemas.FAQCreate,
    current_user: deps.CurrentUser,
    faq_service: FaqService = Depends(),
):
    return faq_service.repository.create_faq(db=faq_service.db, faq=faq_in)


@router.delete("/by_question/{question}", response_model=schemas.FAQ)
def delete_faq_by_question(
    question: str, current_user: deps.CurrentUser, faq_service: FaqService = Depends()
):
    db_faq = faq_service.repository.delete_faq_by_question(faq_service.db, question)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq
