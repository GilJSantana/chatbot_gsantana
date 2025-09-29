from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from chatbot_gsantana.models.user import User
from chatbot_gsantana.schemas.user import UserCreate
from chatbot_gsantana.services.user import user_service


@pytest.fixture
def db_session_mock(mocker: MockerFixture) -> MagicMock:
    """Fixture para mockar a sessão do banco de dados."""
    return mocker.MagicMock()


# CORREÇÃO: Exemplo de um hash argon2 válido para usar nos testes
REALISTIC_HASH = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt8g5o5dJ/A"


def test_authenticate_user_success(db_session_mock, mocker: MockerFixture):
    """Testa a autenticação bem-sucedida de um usuário."""
    mock_user = User(id=1, username="testuser", hashed_password=REALISTIC_HASH)
    mocker.patch(
        "chatbot_gsantana.repositories.user.get_user_by_username",
        return_value=mock_user,
    )
    mocker.patch("chatbot_gsantana.core.security.verify_password", return_value=True)

    authenticated_user = user_service.authenticate_user(
        db_session_mock, username="testuser", password="testpassword"
    )

    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"


def test_authenticate_user_wrong_password(db_session_mock, mocker: MockerFixture):
    """Testa a falha de autenticação com senha incorreta."""
    mock_user = User(id=1, username="testuser", hashed_password=REALISTIC_HASH)
    mocker.patch(
        "chatbot_gsantana.repositories.user.get_user_by_username",
        return_value=mock_user,
    )
    mocker.patch("chatbot_gsantana.core.security.verify_password", return_value=False)

    authenticated_user = user_service.authenticate_user(
        db_session_mock, username="testuser", password="wrongpassword"
    )

    assert authenticated_user is None


def test_authenticate_user_not_found(db_session_mock, mocker: MockerFixture):
    """Testa a falha de autenticação para um usuário inexistente."""
    mocker.patch(
        "chatbot_gsantana.repositories.user.get_user_by_username", return_value=None
    )

    authenticated_user = user_service.authenticate_user(
        db_session_mock, username="nonexistent", password="anypassword"
    )

    assert authenticated_user is None


def test_create_user(db_session_mock, mocker: MockerFixture):
    """Testa a criação de um novo usuário."""
    user_in = UserCreate(username="newuser", password="newpassword")
    mocker.patch(
        "chatbot_gsantana.core.security.get_password_hash", return_value=REALISTIC_HASH
    )

    mock_created_user = User(id=2, username="newuser", hashed_password=REALISTIC_HASH)
    create_user_repo_mock = mocker.patch(
        "chatbot_gsantana.repositories.user.create_user", return_value=mock_created_user
    )

    created_user = user_service.create_user(db_session_mock, user_in=user_in)

    create_user_repo_mock.assert_called_once_with(
        db_session_mock, username="newuser", hashed_password=REALISTIC_HASH
    )
    assert created_user.username == "newuser"
