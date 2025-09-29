import logging
from getpass import getpass

from chatbot_gsantana.core.database import SessionLocal
from chatbot_gsantana.schemas.user import UserCreate
from chatbot_gsantana.services.user import user_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_superuser():
    """Cria um superusuário no banco de dados."""
    logger.info("Iniciando criação de superusuário...")

    db = SessionLocal()
    try:
        username = input("Digite o nome de usuário: ")
        password = getpass("Digite a senha: ")

        user_in = UserCreate(username=username, password=password)
        user = user_service.create_user(db, user_in=user_in)

        logger.info(f"Superusuário '{user.username}' criado com sucesso!")
    except Exception as e:
        logger.error(f"Falha ao criar superusuário: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_superuser()
