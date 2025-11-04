from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from .. import models, schemas
from ..core.config import get_settings
from ..core.database import SessionDep
from ..services.user import UserService

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
    db: SessionDep,
    token: TokenDep,
    user_service: UserService = Depends(),
) -> models.User:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = user_service.repository.get_user_by_username(db, username=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[models.User, Depends(get_current_user)]
