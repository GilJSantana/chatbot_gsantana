import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from pytest import MonkeyPatch

# Importa o módulo 'database' para que possamos substituir seus objetos
from chatbot_gsantana.core import database as database_module
from chatbot_gsantana.main import app
from chatbot_gsantana.core.database import Base, get_db
from chatbot_gsantana.models.user import User
from chatbot_gsantana.core.security import get_password_hash

# 1. Engine de teste que usa um banco de dados SQLite em memória
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 2. Fábrica de sessões de teste que usa o engine de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def override_db_for_tests(monkeypatch: MonkeyPatch):
    """
    Fixture de execução automática que garante que QUALQUER teste que importe
    a aplicação use o banco de dados de teste.
    Esta é a correção definitiva para o problema de ordem de importação.
    """
    monkeypatch.setattr(database_module, "engine", test_engine)
    monkeypatch.setattr(database_module, "SessionLocal", TestingSessionLocal)


@pytest.fixture(scope="function")
def db_session():
    """
    Cria as tabelas, fornece uma sessão de banco de dados de teste e
    depois apaga as tabelas para garantir um estado limpo.
    """
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Fixture que fornece um TestClient com a dependência de banco de dados
    sobrescrita para usar a sessão de teste.
    """
    def override_get_db():
        """Substitui a dependência get_db para usar a sessão de teste."""
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """Cria um usuário de teste no banco de dados de teste."""
    hashed_password = get_password_hash("testpassword")
    user = User(username="testuser", email="test@example.com", hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User) -> dict[str, str]:
    """Gera cabeçalhos de autenticação para um usuário de teste."""
    login_data = {"username": test_user.username, "password": "testpassword"}
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == 200, f"Failed to get token: {response.json()}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}