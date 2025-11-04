from sqlalchemy.orm import Session

from ..models.user import User


class UserRepository:

    def get_user_by_username(self, db: Session, *, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def save(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
