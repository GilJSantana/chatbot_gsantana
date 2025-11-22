import structlog
from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.config import Settings
from ..core.database import get_db
from ..core.security import get_password_hash, verify_password
from ..models.user import User
from ..repositories.user import UserRepository

logger = structlog.get_logger(__name__)


class UserService:

    def __init__(
        self, repository: UserRepository = Depends(), db: Session = Depends(get_db)
    ):
        self.repository = repository
        self.db = db

    def create_user(self, user_data: dict) -> User:
        log = logger.bind(username=user_data["username"])
        log.info("service.user.create.start")
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        db_user = User(**user_data)
        saved_user = self.repository.save(self.db, db_user)
        log.info("service.user.create.success", user_id=saved_user.id)
        return saved_user

    def authenticate_user(self, username: str, password: str) -> User | None:
        db_user = self.repository.get_user_by_username(self.db, username=username)
        if not db_user or not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    def get_or_create_admin_user(self, settings: Settings) -> User:
        admin_username = settings.TEST_ADMIN_USERNAME
        admin_user = self.repository.get_user_by_username(
            self.db, username=admin_username
        )
        if not admin_user:
            logger.info("service.user.admin.creating", username=admin_username)
            user_data = {
                "username": admin_username,
                "email": settings.TEST_ADMIN_EMAIL,
                "password": settings.TEST_ADMIN_PASSWORD,
                "is_admin": True,  # CORREÇÃO: Usa o campo 'is_admin'
            }
            return self.create_user(user_data)

        # Garante que o usuário existente seja um admin
        if not admin_user.is_admin:
            admin_user.is_admin = True
            self.repository.save(self.db, admin_user)

        return admin_user
