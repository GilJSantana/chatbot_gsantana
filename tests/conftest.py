import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from chatbot_gsantana.main import app
from chatbot_gsantana.core.database import get_db, Base
from chatbot_gsantana.core.config import get_settings, Settings
from chatbot_gsantana.models.user import User
from chatbot_gsantana.repositories.user import UserRepository
from chatbot_gsantana.services.user import UserService

# Define o modo de teste antes de qualquer outra importação de configuração
@pytest.fixture(scope="session", autouse=True)
def set_test_mode():
    os.environ["TEST_MODE"] = "1"
    get_settings.cache_clear()
    yield
    os.environ.pop("TEST_MODE", None)
    get_settings.cache_clear()

@pytest.fixture(scope="session")
def test_settings() -> Settings:
    return get_settings()

@pytest.fixture(scope="session")
def test_engine(test_settings: Settings):
    engine = create_engine(str(test_settings.DATABASE_URL), connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def TestingSessionLocal(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def db_session(test_engine, TestingSessionLocal):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session) -> User:
    """Cria um usuário de teste para autenticação."""
    user_repo = UserRepository()
    user_service = UserService(repository=user_repo, db=db_session)
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com"
    }
    return user_service.create_user(user_data=user_data)

@pytest.fixture(scope="function")
def auth_headers(client, test_user: User) -> dict:
    """Obtém um token de autenticação para o usuário de teste."""
    response = client.post(
        app.url_path_for("login_for_access_token"),
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200, f"Falha ao obter token: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
