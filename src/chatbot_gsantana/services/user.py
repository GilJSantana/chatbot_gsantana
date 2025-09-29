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
        """Cria um novo usuário."""
        hashed_password = security.get_password_hash(user_in.password)
        db_user = user_repository.create_user(
            db, username=user_in.username, hashed_password=hashed_password
        )
        return db_user


user_service = UserService()
