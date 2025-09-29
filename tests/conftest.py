import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# CORREÇÃO: Imports diretos do pacote, sem o prefixo 'src'
from chatbot_gsantana.api.deps import get_db
from chatbot_gsantana.core.database import Base
from chatbot_gsantana.main import app
from chatbot_gsantana.schemas import UserCreate
from chatbot_gsantana.services.user import user_service

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados de teste e limpa as tabelas."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste para a API, usando o banco de dados de teste."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Cria um usuário de teste no banco de dados."""
    user_in = UserCreate(username="testuser", password="testpassword")
    return user_service.create_user(db=db_session, user_in=user_in)


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user):
    """Autentica o usuário de teste e retorna os cabeçalhos de autorização."""
    login_data = {"username": test_user.username, "password": "testpassword"}
    response = client.post("/api/v1/token", data=login_data)
    assert response.status_code == 200, "Falha ao fazer login durante o teste"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
