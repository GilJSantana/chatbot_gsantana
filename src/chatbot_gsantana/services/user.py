from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..core import security
from ..repositories import user as user_repository


class UserService:
    """Camada de serviço para a lógica de negócio dos usuários."""

    def authenticate_user(
        self, db: Session, *, username: str, password: str
    ) -> models.User | None:
        """Autentica um usuário."""
        user = user_repository.get_user_by_username(db, username=username)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    def create_user(self, db: Session, *, user_in: schemas.UserCreate) -> models.User:
        """
        Cria um novo usuário após validar se o username e email já existem.
        """
        db_user_by_username = user_repository.get_user_by_username(
            db, username=user_in.username
        )
        if db_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        db_user_by_email = user_repository.get_user_by_email(db, email=user_in.email)
        if db_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = security.get_password_hash(user_in.password)
        db_user = user_repository.create_user(
            db,
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
        )
        
        # CORREÇÃO: Confirma (commit) a transação para salvar o usuário no banco de dados.
        db.commit()
        db.refresh(db_user)
        
        return db_user


user_service = UserService()
