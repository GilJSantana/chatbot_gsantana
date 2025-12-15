import pytest
import sys
from contextlib import contextmanager

import manage as manage_module
from chatbot_gsantana.models.user import User
from sqlalchemy.orm import Session


@pytest.fixture(autouse=True)
def mock_cli_db(monkeypatch, db_session: Session):
    """
    Substitui a função get_session do manage.py por uma que retorna
    a sessão de teste em memória, garantindo isolamento total da rede.
    """

    @contextmanager
    def mock_get_session():
        yield db_session

    monkeypatch.setattr(manage_module, "get_session", mock_get_session)


def run_cli_command(monkeypatch, command_args):
    """
    Helper para executar o script manage.py com argumentos.
    """
    monkeypatch.setattr(sys, "argv", ["manage.py"] + command_args)
    manage_module.main()


# --- Testes para 'create-user' ---


def test_create_user_as_admin_success(capsys, monkeypatch, db_session: Session):
    """Testa o caminho feliz da criação de um usuário administrador."""
    monkeypatch.delenv("TEST_ADMIN_PASSWORD", raising=False)

    inputs = iter(["testpassword", "testpassword"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))

    run_cli_command(
        monkeypatch, ["create-user", "newadmin", "admin@test.com", "--admin"]
    )

    captured = capsys.readouterr()
    assert (
        "✅ Usuário 'newadmin' criado com sucesso como administrador!" in captured.out
    )

    user = db_session.query(User).filter(User.username == "newadmin").first()
    assert user is not None
    assert user.is_admin is True


def test_create_user_as_common_success(capsys, monkeypatch, db_session: Session):
    """Testa o caminho feliz da criação de um usuário comum."""
    monkeypatch.delenv("TEST_ADMIN_PASSWORD", raising=False)

    inputs = iter(["testpassword", "testpassword"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))

    run_cli_command(monkeypatch, ["create-user", "newcommon", "common@test.com"])

    captured = capsys.readouterr()
    assert "✅ Usuário 'newcommon' criado com sucesso como comum!" in captured.out

    user = db_session.query(User).filter(User.username == "newcommon").first()
    assert user is not None
    assert user.is_admin is False


def test_create_user_password_mismatch(capsys, monkeypatch):
    """Testa o cenário onde as senhas não coincidem."""
    monkeypatch.delenv("TEST_ADMIN_PASSWORD", raising=False)

    inputs = iter(["pass1", "pass2"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))

    run_cli_command(monkeypatch, ["create-user", "anotheruser", "another@test.com"])

    captured = capsys.readouterr()
    assert "As senhas não coincidem" in captured.out


def test_create_user_username_already_exists(capsys, monkeypatch, test_user: User):
    """Testa o cenário onde o nome de usuário já existe."""
    inputs = iter(["password", "password"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))

    run_cli_command(
        monkeypatch, ["create-user", test_user.username, "newemail@test.com"]
    )

    captured = capsys.readouterr()
    assert f">> Erro: O usuário '{test_user.username}' já existe." in captured.out


def test_create_user_email_already_exists(capsys, monkeypatch, test_user: User):
    """NOVO TESTE: Testa o cenário onde o email já está em uso."""
    inputs = iter(["password", "password"])
    monkeypatch.setattr("getpass.getpass", lambda prompt: next(inputs))

    # Tenta criar um usuário com um NOVO username, mas o MESMO email da fixture
    run_cli_command(monkeypatch, ["create-user", "newuser_same_email", test_user.email])

    captured = capsys.readouterr()
    assert f">> Erro: O email '{test_user.email}' já está em uso." in captured.out


# --- Testes para 'list-users' ---


def test_list_users(capsys, monkeypatch, test_user: User):
    """Testa se a listagem de usuários funciona corretamente."""
    run_cli_command(monkeypatch, ["list-users"])

    captured = capsys.readouterr()
    assert "Listando todos os usuários..." in captured.out
    assert test_user.username in captured.out


# --- Testes para 'promote-user' e 'demote-user' ---


def test_promote_user(capsys, monkeypatch, db_session: Session):
    """Testa a promoção de um usuário comum para administrador."""
    from chatbot_gsantana.core.security import get_password_hash

    user = User(
        username="commonuser",
        email="common@test.com",
        hashed_password=get_password_hash("pass"),
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()

    run_cli_command(monkeypatch, ["promote-user", "commonuser"])

    captured = capsys.readouterr()
    assert "✅ Usuário 'commonuser' promovido a administrador." in captured.out

    db_session.refresh(user)
    assert user.is_admin is True


def test_demote_user(capsys, monkeypatch, db_session: Session, test_user: User):
    """Testa o rebaixamento de um administrador para usuário comum."""
    assert test_user.is_admin is True

    run_cli_command(monkeypatch, ["demote-user", test_user.username])

    captured = capsys.readouterr()
    assert (
        f"✅ Usuário '{test_user.username}' rebaixado para usuário comum."
        in captured.out
    )

    db_session.refresh(test_user)
    assert test_user.is_admin is False
