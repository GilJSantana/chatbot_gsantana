from sqlalchemy.orm import Session

from ..models.user import User


def get_user_by_username(db: Session, *, username: str) -> User | None:
    """Busca um usuário pelo nome de usuário."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, *, username: str, hashed_password: str) -> User:
    """Cria um novo usuário no banco de dados."""
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
