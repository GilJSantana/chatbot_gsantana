import logging
from getpass import getpass

from chatbot_gsantana.core.database import SessionLocal
from chatbot_gsantana.core import security
from chatbot_gsantana.repositories import user as user_repository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_superuser():
    """Cria um superusuário no banco de dados de forma interativa."""
    logger.info("Iniciando criação de superusuário...")
    db = SessionLocal()
    try:
        username = input("Digite o nome de usuário: ")
        email = input("Digite o email: ")

        existing_user = user_repository.get_user_by_username(db, username=username)
        if existing_user:
            logger.error(f"Usuário '{username}' já existe. Abortando.")
            return

        password = getpass("Digite a senha: ")
        confirm_password = getpass("Confirme a senha: ")

        if password != confirm_password:
            logger.error("As senhas não coincidem. Abortando.")
            return

        hashed_password = security.get_password_hash(password)

        user_repository.create_user(
            db,
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

        # CORREÇÃO: Confirma (commit) a transação para salvar o usuário no banco de dados.
        db.commit()

        logger.info(f"Superusuário '{username}' criado com sucesso!")

    except Exception as e:
        logger.error(f"Falha ao criar superusuário: {e}")
        db.rollback() # Desfaz a transação em caso de erro
    finally:
        db.close()


if __name__ == "__main__":
    create_superuser()
