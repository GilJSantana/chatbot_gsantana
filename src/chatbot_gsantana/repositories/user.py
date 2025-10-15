from sqlalchemy.orm import Session

from ..models.user import User


def get_user_by_username(db: Session, *, username: str) -> User | None:
    """Busca um usuário pelo nome de usuário."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, *, email: str) -> User | None:
    """Busca um usuário pelo email."""
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session, *, username: str, email: str, hashed_password: str
) -> User:
    """Cria um novo usuário no banco de dados, incluindo o email."""
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.flush()
    db.refresh(db_user)
    return db_user
