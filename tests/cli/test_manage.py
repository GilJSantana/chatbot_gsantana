import pytest
import sys

from chatbot_gsantana.manage import main
from chatbot_gsantana.models.user import User
from sqlalchemy.orm import Session

# --- Fixtures ---


@pytest.fixture(autouse=True)
def mock_db_connection(monkeypatch):
    """
    Impede que o manage.py tente se conectar ao banco de dados real,
    usando o banco de dados de teste em memória das outras fixtures.
    """
    # Esta fixture é necessária para garantir que o motor do banco de dados
    # criado no manage.py não seja usado. Os testes usarão o db_session.
    pass


# --- Testes para 'create-admin' ---


def test_create_admin_success(capsys, monkeypatch, db_session: Session):
    """
    Testa o caminho feliz da criação de um administrador.
    """
    # Simula a entrada do usuário para a senha
    inputs = iter(["testpassword", "testpassword"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))

    # Simula os argumentos de linha de comando
    monkeypatch.setattr(
        sys, "argv", ["manage.py", "create-admin", "newadmin", "admin@test.com"]
    )

    main()

    # Captura a saída do console
    captured = capsys.readouterr()
    assert "✅ Administrador 'newadmin' criado com sucesso!" in captured.out

    # Verifica no banco de dados
    user = db_session.query(User).filter(User.username == "newadmin").first()
    assert user is not None
    assert user.email == "admin@test.com"
    assert user.is_admin is True


def test_create_admin_password_mismatch(capsys, monkeypatch):
    """
    Testa o cenário onde as senhas não coincidem.
    """
    inputs = iter(["pass1", "pass2"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))
    monkeypatch.setattr(
        sys, "argv", ["manage.py", "create-admin", "anotheradmin", "another@test.com"]
    )

    main()

    captured = capsys.readouterr()
    assert "As senhas não coincidem" in captured.out


def test_create_admin_user_already_exists(
    capsys, monkeypatch, db_session: Session, test_user: User
):
    """
    Testa o cenário onde o nome de usuário já existe.
    """
    inputs = iter(["password", "password"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))
    # Tenta criar um usuário com o mesmo username da fixture 'test_user'
    monkeypatch.setattr(
        sys,
        "argv",
        ["manage.py", "create-admin", test_user.username, "newemail@test.com"],
    )

    main()

    captured = capsys.readouterr()
    assert f"Erro: O usuário '{test_user.username}' já existe" in captured.out


# --- Testes para 'list-users' ---


def test_list_users(capsys, monkeypatch, db_session: Session, test_user: User):
    """
    Testa se a listagem de usuários funciona corretamente.
    """
    monkeypatch.setattr(sys, "argv", ["manage.py", "list-users"])

    main()

    captured = capsys.readouterr()
    assert "Listando todos os usuários..." in captured.out
    assert test_user.username in captured.out
    assert test_user.email in captured.out
    assert "Yes" in captured.out  # Porque o test_user é admin


# --- Testes para 'promote-user' e 'demote-user' ---


def test_promote_user(capsys, monkeypatch, db_session: Session):
    """
    Testa a promoção de um usuário comum para administrador.
    """
    # Cria um usuário não-admin primeiro
    from chatbot_gsantana.core.security import get_password_hash

    user = User(
        username="commonuser",
        email="common@test.com",
        hashed_password=get_password_hash("pass"),
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()

    monkeypatch.setattr(sys, "argv", ["manage.py", "promote-user", "commonuser"])
    main()

    captured = capsys.readouterr()
    assert "✅ Usuário 'commonuser' promovido a administrador." in captured.out

    db_session.refresh(user)
    assert user.is_admin is True


def test_demote_user(capsys, monkeypatch, db_session: Session, test_user: User):
    """
    Testa o rebaixamento de um administrador para usuário comum.
    """
    # O test_user da fixture é admin por padrão
    assert test_user.is_admin is True

    monkeypatch.setattr(sys, "argv", ["manage.py", "demote-user", test_user.username])
    main()

    captured = capsys.readouterr()
    assert (
        f"✅ Usuário '{test_user.username}' rebaixado para usuário comum."
        in captured.out
    )

    db_session.refresh(test_user)
    assert test_user.is_admin is False
