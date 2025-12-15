from sqlalchemy.orm import Session
from typing import List

from ..models.user import User


class UserRepository:
    """
    Encapsula a lógica de acesso a dados para o modelo User.
    """

    def get_user_by_username(self, db: Session, username: str) -> User | None:
        """Busca um usuário pelo nome de usuário."""
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        """Busca um usuário pelo email."""
        return db.query(User).filter(User.email == email).first()

    def get_all_users(self, db: Session) -> List[User]:
        """Busca todos os usuários."""
        return db.query(User).all()

    def save(self, db: Session, user: User) -> User:
        """Salva um novo usuário ou atualiza um existente."""
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
