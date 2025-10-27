from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from .. import models, schemas
from ..core.config import get_settings
from ..core.database import SessionDep
from ..repositories import user as user_repository

# --- Segurança / Autenticação ---

# O prefixo da API é definido diretamente para evitar o erro de configuração nos testes.
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(db: SessionDep, token: TokenDep) -> models.User:
    """Valida o token JWT e retorna o usuário correspondente."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # O campo 'sub' (subject) do token contém o nome de usuário.
        token_data = schemas.TokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # Busca o usuário no banco de dados usando o 'sub' do token.
    user = user_repository.get_user_by_username(db, username=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[models.User, Depends(get_current_user)]
