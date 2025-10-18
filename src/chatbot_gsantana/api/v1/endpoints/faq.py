from fastapi import APIRouter, status, HTTPException

from chatbot_gsantana import schemas
from chatbot_gsantana.api import deps
from chatbot_gsantana.services.faq import faq_service

router = APIRouter()


@router.get("/", response_model=list[schemas.FAQ])
def get_faqs(db: deps.SessionDep, skip: int = 0, limit: int = 100):
    """Busca todas as FAQs."""
    return faq_service.get_faqs(db, skip=skip, limit=limit)


@router.get("/{faq_id}", response_model=schemas.FAQ)
def get_faq(faq_id: int, db: deps.SessionDep):
    """Busca uma FAQ pelo ID."""
    db_faq = faq_service.get_faq(db, faq_id=faq_id)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq


@router.post(
    "/",
    response_model=schemas.FAQ,
    status_code=status.HTTP_201_CREATED,
)
def create_faq(
    faq_in: schemas.FAQCreate, db: deps.SessionDep, current_user: deps.CurrentUser
):
    """Cria uma nova FAQ (requer autenticação)."""
    return faq_service.create_faq(db=db, faq=faq_in)
