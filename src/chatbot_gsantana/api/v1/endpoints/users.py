from fastapi import APIRouter, status, Depends

from chatbot_gsantana import schemas
from chatbot_gsantana.api import deps
from chatbot_gsantana.services.user import UserService

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_in: schemas.UserCreate, user_service: UserService = Depends()):
    user = user_service.create_user(user_data=user_in.dict())
    return user


@router.get("/me", response_model=schemas.User)
def read_current_user(current_user: deps.CurrentUser):
    return current_user
