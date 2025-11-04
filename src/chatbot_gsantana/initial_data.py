import structlog

from chatbot_gsantana.core.config import get_settings
from chatbot_gsantana.core.database import get_db_session_factory, Base
from chatbot_gsantana.services.user import get_user_service

logger = structlog.get_logger(__name__)


def main() -> None:
    logger.info("Initializing service...")
    settings = get_settings()
    session_factory = get_db_session_factory(str(settings.DATABASE_URL))
    engine = session_factory.kw["bind"]

    logger.info("Creating initial database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema created.")

    # Cria o usuário admin se as variáveis de ambiente estiverem definidas
    if settings.TEST_ADMIN_USERNAME:
        logger.info(
            "Creating initial admin user for testing...",
            username=settings.TEST_ADMIN_USERNAME,
        )
        with session_factory() as db:
            user_service = get_user_service()
            user_service.get_or_create_admin_user(db, settings)
        logger.info("Initial admin user created.")

    logger.info("Service initialization finished.")


if __name__ == "__main__":
    main()
