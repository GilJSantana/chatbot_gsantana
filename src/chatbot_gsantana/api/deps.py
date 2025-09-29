from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .. import models, schemas
from ..core.config import settings
from ..repositories import user as user_repository

# --- Conexão com o Banco de Dados ---

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Dependência para obter uma sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]

# --- Segurança e Autenticação ---

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(db: SessionDep, token: TokenDep) -> models.User:
    """Dependência para obter o usuário atual a partir do token JWT."""
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
    user = user_repository.get_user_by_username(db, username=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[models.User, Depends(get_current_user)]
