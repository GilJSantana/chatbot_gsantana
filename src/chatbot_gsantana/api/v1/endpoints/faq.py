from fastapi import APIRouter, HTTPException

from .... import schemas
from ....api.deps import CurrentUser, SessionDep
from ....services.faq import faq_service

router = APIRouter()


@router.post("/", response_model=schemas.FAQ)
def create_faq(*, db: SessionDep, faq_in: schemas.FAQCreate, current_user: CurrentUser):
    """Cria uma nova FAQ (requer autenticação)."""
    return faq_service.create_faq(db=db, faq=faq_in)


@router.get("/", response_model=list[schemas.FAQ])
def read_faqs(db: SessionDep, skip: int = 0, limit: int = 100):
    """Lista todas as FAQs (público)."""
    return faq_service.get_faqs(db=db, skip=skip, limit=limit)


@router.get("/{faq_id}", response_model=schemas.FAQ)
def read_faq(*, db: SessionDep, faq_id: int):
    """Busca uma FAQ pelo ID (público)."""
    db_faq = faq_service.get_faq(db=db, faq_id=faq_id)
    if db_faq is None:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq


@router.put("/{faq_id}", response_model=schemas.FAQ)
def update_faq(
    *, db: SessionDep, faq_id: int, faq_in: schemas.FAQCreate, current_user: CurrentUser
):
    """Atualiza uma FAQ (requer autenticação)."""
    db_faq = faq_service.get_faq(db=db, faq_id=faq_id)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    db_faq = faq_service.update_faq(db=db, faq_id=faq_id, faq=faq_in)
    return db_faq


@router.delete("/{faq_id}", response_model=schemas.FAQ)
def delete_faq(*, db: SessionDep, faq_id: int, current_user: CurrentUser):
    """Deleta uma FAQ (requer autenticação)."""
    db_faq = faq_service.get_faq(db=db, faq_id=faq_id)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    db_faq = faq_service.delete_faq(db=db, faq_id=faq_id)
    return db_faq
