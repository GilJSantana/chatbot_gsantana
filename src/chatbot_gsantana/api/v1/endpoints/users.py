from fastapi import APIRouter, status

from chatbot_gsantana import schemas
from chatbot_gsantana.api import deps
from chatbot_gsantana.services.user import user_service

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_in: schemas.UserCreate, db: deps.SessionDep):
    """Cria um novo usuário."""
    # Idealmente, este endpoint deveria ser protegido ou removido em produção.
    user = user_service.create_user(db=db, user_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: deps.CurrentUser):
    """Obtém os dados do usuário atualmente autenticado."""
    return current_user
