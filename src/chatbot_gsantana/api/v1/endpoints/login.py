from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .... import schemas
from ....api import deps
from ....core import security
from ....core.config import get_settings
from ....services.user import user_service

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: deps.SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Autentica o usuário e retorna um token de acesso."""
    user = user_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
