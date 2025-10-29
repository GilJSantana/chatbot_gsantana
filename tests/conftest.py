import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator

from chatbot_gsantana.core.config import get_settings, Settings
from chatbot_gsantana.core.database import Base, get_db
from chatbot_gsantana.main import create_app


@pytest.fixture(scope="session", autouse=True)
def clear_settings_cache_for_tests():
    """
    Limpa o cache da função get_settings() antes de iniciar a sessão de testes.
    Isso garante que as configurações de teste sejam recarregadas corretamente.
    """
    get_settings.cache_clear()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Fixture que conecta ao banco de dados de teste (SQLite em memória),
    cria as tabelas, fornece uma sessão e depois limpa tudo.
    """
    # Garante que a URL do banco de dados de teste seja usada
    test_database_url = "sqlite:///./test.db"

    # Cria um engine e uma SessionLocal específicos para o teste
    test_engine = create_engine(test_database_url, pool_pre_ping=True)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Cria um TestClient com uma aplicação limpa para cada teste,
    sobrescrevendo as dependências do banco de dados e configurações.
    """
    # 1. Cria uma instância de Settings para o ambiente de teste
    test_settings = Settings(DATABASE_URL="sqlite:///./test.db")

    # 2. Cria a aplicação, passando as configurações de teste diretamente
    app = create_app(settings=test_settings)

    # 3. Sobrescreve a dependência get_db para usar a sessão de teste
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # 4. Inicia o TestClient
    with TestClient(app) as c:
        yield c

    # 5. Limpa os overrides após o teste
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    """
    Cria um usuário de teste no banco de dados de teste.
    """
    from chatbot_gsantana.models.user import User
    from chatbot_gsantana.core.security import get_password_hash

    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser", email="test@example.com", hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client: TestClient, test_user) -> dict[str, str]:
    """
    Gera cabeçalhos de autenticação para um usuário de teste.
    """
    login_data = {"username": test_user.username, "password": "testpassword"}
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == 200, f"Falha ao obter token: {response.json()}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
