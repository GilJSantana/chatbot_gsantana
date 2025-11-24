import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from chatbot_gsantana.main import app
from chatbot_gsantana.core.database import Base, get_db
from chatbot_gsantana.services.user import UserService
from chatbot_gsantana.repositories.user import UserRepository
from chatbot_gsantana.models.user import User

# --- Carregamento Explícito do .env.e2e ---
print("Carregando variáveis de ambiente do .env.e2e...")
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env.e2e")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
    print("Arquivo .env.e2e carregado com sucesso.")
else:
    print("Aviso: Arquivo .env.e2e não encontrado.")


# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """Fixture para fornecer uma sessão de banco de dados de teste."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """Fixture para o TestClient do FastAPI com override do banco de dados."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """Fixture que cria um usuário de teste no banco de dados."""
    user_repo = UserRepository()
    user_service = UserService(repository=user_repo, db=db_session)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "is_admin": True,
    }
    user = user_service.create_user(user_data=user_data)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user: User) -> dict:
    """Fixture que obtém um token de autenticação para o usuário de teste."""
    login_data = {
        "username": test_user.username,
        "password": "testpassword",
    }
    response = client.post("/api/v1/auth/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
