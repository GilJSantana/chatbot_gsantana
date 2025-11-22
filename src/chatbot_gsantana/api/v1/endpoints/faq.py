from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from chatbot_gsantana import schemas
from chatbot_gsantana.api import deps
from chatbot_gsantana.services.faq import FaqService

router = APIRouter()


@router.get("/", response_model=List[schemas.FAQ])
def get_faqs(
    current_user: deps.CurrentAdminUser,
    faq_service: FaqService = Depends(),
    skip: int = 0,
    limit: int = 100,
):
    """Busca todas as FAQs (requer autenticação de admin)."""
    return faq_service.repository.get_faqs(faq_service.db, skip=skip, limit=limit)


@router.get("/{faq_id}", response_model=schemas.FAQ)
def get_faq(
    faq_id: int,
    current_user: deps.CurrentAdminUser,
    faq_service: FaqService = Depends(),
):
    """Busca uma FAQ pelo ID (requer autenticação de admin)."""
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
    current_user: deps.CurrentAdminUser,
    faq_service: FaqService = Depends(),
):
    """Cria uma nova FAQ (requer autenticação de admin)."""
    return faq_service.repository.create_faq(db=faq_service.db, faq=faq_in)


@router.put("/{faq_id}", response_model=schemas.FAQ)
def update_faq(
    faq_id: int,
    faq_in: schemas.FAQUpdate,
    current_user: deps.CurrentAdminUser,
    faq_service: FaqService = Depends(),
):
    """Atualiza uma FAQ (requer autenticação de admin)."""
    db_faq = faq_service.repository.update_faq(faq_service.db, faq_id, faq_in)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq


@router.delete("/{faq_id}", response_model=schemas.FAQ)
def delete_faq(
    faq_id: int,
    current_user: deps.CurrentAdminUser,
    faq_service: FaqService = Depends(),
):
    """Exclui uma FAQ (requer autenticação de admin)."""
    db_faq = faq_service.repository.delete_faq(faq_service.db, faq_id)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq
