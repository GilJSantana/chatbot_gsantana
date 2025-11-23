import argparse
import getpass
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from chatbot_gsantana.core.config import get_settings
from chatbot_gsantana.services.user import UserService
from chatbot_gsantana.repositories.user import UserRepository


# --- Configuração do Banco de Dados ---
settings = get_settings()
engine = create_engine(str(settings.DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Funções dos Comandos ---

def create_admin(args):
    """Cria um novo usuário administrador."""
    print(f"Criando administrador '{args.username}'...")
    password = getpass.getpass("Digite a senha: ")
    password_confirm = getpass.getpass("Confirme a senha: ")

    if password != password_confirm:
        print(">> As senhas não coincidem. Operação cancelada.")
        return

    with SessionLocal() as db:
        user_repo = UserRepository()
        user_service = UserService(repository=user_repo, db=db)
        existing_user = user_service.repository.get_user_by_username(
            db, username=args.username
        )
        if existing_user:
            print(f">> Erro: O usuário '{args.username}' já existe.")
            return

        user_data = {
            "username": args.username,
            "email": args.email,
            "password": password,
            "is_admin": True,
        }
        try:
            user_service.create_user(user_data)
            print(f"✅ Administrador '{args.username}' criado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar administrador: {e}")


def list_users(args):
    """Lista todos os usuários no banco de dados."""
    print("Listando todos os usuários...")
    with SessionLocal() as db:
        user_repo = UserRepository()
        users = user_repo.get_all_users(db)

        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Is Admin'}")
        print("-" * 65)
        for user in users:
            is_admin_str = "Yes" if user.is_admin else "No"
            print(f"{user.id:<5} {user.username:<20} {user.email:<30} {is_admin_str}")


def promote_user(args):
    """Promove um usuário a administrador."""
    with SessionLocal() as db:
        user_repo = UserRepository()
        user = user_repo.get_user_by_username(db, username=args.username)
        if not user:
            print(f">> Erro: Usuário '{args.username}' não encontrado.")
            return

        user.is_admin = True
        user_repo.save(db, user)
        print(f"✅ Usuário '{args.username}' promovido a administrador.")


def demote_user(args):
    """Rebaixa um administrador para usuário comum."""
    with SessionLocal() as db:
        user_repo = UserRepository()
        user = user_repo.get_user_by_username(db, username=args.username)
        if not user:
            print(f">> Erro: Usuário '{args.username}' não encontrado.")
            return

        user.is_admin = False
        user_repo.save(db, user)
        print(f"✅ Usuário '{args.username}' rebaixado para usuário comum.")


# --- Configuração do Parser de Argumentos ---

def main():
    """Função principal para configurar e executar a CLI."""
    parser = argparse.ArgumentParser(
        description="Ferramenta de linha de comando para gerenciar a aplicação."
    )
    subparsers = parser.add_subparsers(
        dest='command', required=True, help='Sub-comando a ser executado'
    )

    # Comando create-admin
    parser_create = subparsers.add_parser(
        'create-admin', help='Cria um novo usuário administrador.'
    )
    parser_create.add_argument(
        'username', type=str, help='Nome de usuário para o novo administrador.'
    )
    parser_create.add_argument(
        'email', type=str, help='Email para o novo administrador.'
    )
    parser_create.set_defaults(func=create_admin)

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
