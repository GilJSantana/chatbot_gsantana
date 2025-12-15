import argparse
import getpass
import os
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from chatbot_gsantana.core.config import get_settings
from chatbot_gsantana.services.user import UserService
from chatbot_gsantana.repositories.user import UserRepository
from chatbot_gsantana.core.database import Base


@contextmanager
def get_session():
    """Fornece uma sessão de banco de dados para os comandos da CLI."""
    settings = get_settings()
    engine = create_engine(str(settings.DATABASE_URL))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(args):
    """Cria todas as tabelas no banco de dados."""
    print("Inicializando o banco de dados...")
    settings = get_settings()
    engine = create_engine(str(settings.DATABASE_URL))
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso.")


def create_user(args):
    """Cria um novo usuário (comum ou administrador)."""
    is_admin = args.admin
    user_type = "administrador" if is_admin else "comum"
    print(f"Criando usuário '{args.username}' como {user_type}...")

    password = os.getenv("TEST_ADMIN_PASSWORD")
    if not password:
        print("Variável de ambiente TEST_ADMIN_PASSWORD não encontrada.")
        password = getpass.getpass("Digite a senha: ")
        password_confirm = getpass.getpass("Confirme a senha: ")
        if password != password_confirm:
            print(">> As senhas não coincidem. Operação cancelada.")
            return
    else:
        print("Senha encontrada na variável de ambiente.")

    with get_session() as db:
        user_repo = UserRepository()
        user_service = UserService(repository=user_repo, db=db)

        # CORREÇÃO: Verifica se o username ou o email já existem
        if user_repo.get_user_by_username(db, username=args.username):
            print(f">> Erro: O usuário '{args.username}' já existe.")
            return
        if user_repo.get_user_by_email(db, email=args.email):
            print(f">> Erro: O email '{args.email}' já está em uso.")
            return

        user_data = {
            "username": args.username,
            "email": args.email,
            "password": password,
            "is_admin": is_admin,
        }
        try:
            user_service.create_user(user_data)
            print(f"✅ Usuário '{args.username}' criado com sucesso como {user_type}!")
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")


def list_users(args):
    """Lista todos os usuários no banco de dados."""
    print("Listando todos os usuários...")
    with get_session() as db:
        user_repo = UserRepository()
        users = user_repo.get_all_users(db)

        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Is Admin'}")
        print("-" * 65)
        for db_user in users:
            is_admin_str = "Yes" if db_user.is_admin else "No"
            print(
                f"{db_user.id:<5} {db_user.username:<20} "
                f"{db_user.email:<30} {is_admin_str}"
            )


def promote_user(args):
    """Promove um usuário a administrador."""
    with get_session() as db:
        user_repo = UserRepository()
        user_to_promote = user_repo.get_user_by_username(db, username=args.username)
        if not user_to_promote:
            print(f">> Erro: Usuário '{args.username}' não encontrado.")
            return

        user_to_promote.is_admin = True
        user_repo.save(db, user_to_promote)
        print(f"✅ Usuário '{args.username}' promovido a administrador.")


def demote_user(args):
    """Rebaixa um administrador para usuário comum."""
    with get_session() as db:
        user_repo = UserRepository()
        user_to_demote = user_repo.get_user_by_username(db, username=args.username)
        if not user_to_demote:
            print(f">> Erro: Usuário '{args.username}' não encontrado.")
            return

        user_to_demote.is_admin = False
        user_repo.save(db, user_to_demote)
        print(f"✅ Usuário '{args.username}' rebaixado para usuário comum.")


def main():
    """Função principal para configurar e executar a CLI."""
    parser = argparse.ArgumentParser(
        description="Ferramenta de linha de comando para gerenciar a aplicação."
    )
    subparsers = parser.add_subparsers(
        dest='command', required=True, help='Sub-comando a ser executado'
    )

    # Comando init-db
    parser_init_db = subparsers.add_parser(
        'init-db', help='Cria todas as tabelas no banco de dados.'
    )
    parser_init_db.set_defaults(func=init_db)

    # Comando create-user
    parser_create_user = subparsers.add_parser(
        'create-user', help='Cria um novo usuário (comum ou administrador).'
    )
    parser_create_user.add_argument(
        'username', type=str, help='Nome de usuário para o novo usuário.'
    )
    parser_create_user.add_argument('email', type=str, help='Email do novo usuário.')
    parser_create_user.add_argument(
        '--admin', action='store_true', help='Define o usuário como administrador.'
    )
    parser_create_user.set_defaults(func=create_user)

    # Comando list-users
    parser_list = subparsers.add_parser('list-users', help='Lista todos os usuários.')
    parser_list.set_defaults(func=list_users)

    # Comando promote-user
    parser_promote = subparsers.add_parser(
        'promote-user', help='Promove um usuário a administrador.'
    )
    parser_promote.add_argument(
        'username', type=str, help='Nome de usuário a ser promovido.'
    )
    parser_promote.set_defaults(func=promote_user)

    # Comando demote-user
    parser_demote = subparsers.add_parser(
        'demote-user', help='Rebaixa um administrador para usuário comum.'
    )
    parser_demote.add_argument(
        'username', type=str, help='Nome de usuário a ser rebaixado.'
    )
    parser_demote.set_defaults(func=demote_user)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
