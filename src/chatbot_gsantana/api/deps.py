from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from chatbot_gsantana.core.config import get_settings
from chatbot_gsantana.core.database import get_db
from chatbot_gsantana.models.user import User
from chatbot_gsantana.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

settings = get_settings()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_repo.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependência que verifica se o usuário autenticado é um administrador.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdminUser = Annotated[User, Depends(get_current_admin_user)]
