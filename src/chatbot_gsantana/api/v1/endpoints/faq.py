from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import schemas
from ....api import deps
from ....services.faq import faq_service

router = APIRouter()


@router.post("/", response_model=schemas.FAQ)
def create_faq(faq: schemas.FAQCreate, db: Session = Depends(deps.get_db)):
    """Cria uma nova FAQ."""
    return faq_service.create_faq(db=db, faq=faq)


@router.get("/", response_model=list[schemas.FAQ])
def read_faqs(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """Lista todas as FAQs."""
    return faq_service.get_faqs(db=db, skip=skip, limit=limit)


@router.get("/{faq_id}", response_model=schemas.FAQ)
def read_faq(faq_id: int, db: Session = Depends(deps.get_db)):
    """Busca uma FAQ pelo ID."""
    db_faq = faq_service.get_faq(db=db, faq_id=faq_id)
    if db_faq is None:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq


@router.put("/{faq_id}", response_model=schemas.FAQ)
def update_faq(faq_id: int, faq: schemas.FAQCreate, db: Session = Depends(deps.get_db)):
    """Atualiza uma FAQ."""
    db_faq = faq_service.update_faq(db=db, faq_id=faq_id, faq=faq)
    if db_faq is None:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq


@router.delete("/{faq_id}", response_model=schemas.FAQ)
def delete_faq(faq_id: int, db: Session = Depends(deps.get_db)):
    """Deleta uma FAQ."""
    db_faq = faq_service.delete_faq(db=db, faq_id=faq_id)
    if db_faq is None:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return db_faq
