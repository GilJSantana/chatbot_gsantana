import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from chatbot_gsantana.main import app
from chatbot_gsantana.core.database import Base, get_db
from chatbot_gsantana.models.user import User
from chatbot_gsantana.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Cria uma fábrica de sessões para os testes
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Esta é a fixture principal que gerencia
    o ciclo de vida do banco de dados para cada teste.
    Ela garante que cada teste rode em
    uma transação isolada que é revertida no final.
    """
    # 1. Cria uma conexão única para a duração do teste.
    # Esta conexão será compartilhada
    # entre o thread do teste e os threads dos endpoints do FastAPI.
    connection = engine.connect()
    # 2. Inicia uma transação.
    transaction = connection.begin()
    # 3. Cria as tabelas dentro desta transação.
    Base.metadata.create_all(bind=connection)

    # 4. Salva o bind original da fábrica de sessões.
    original_bind = TestingSessionLocal.kw["bind"]
    # 5. Reconfigura a fábrica para usar ESTA conexão específica durante o teste.
    # Isso garante que a sessão criada
    # no endpoint da API use a mesma transação do teste.
    TestingSessionLocal.configure(bind=connection)

    # 6. Cria uma sessão para ser usada
    # diretamente nas fixtures e nos testes (ex: para setup).
    session = TestingSessionLocal()

    # 7. Entrega a sessão para o teste.
    yield session

    # 8. Limpeza após o teste.
    session.close()
    # 9. Restaura o bind original da fábrica de sessões para garantir isolamento.
    TestingSessionLocal.configure(bind=original_bind)
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Fixture que fornece um TestClient com a dependência de banco de dados
    sobrescrita para usar a sessão de teste.
    """

    def override_get_db():
        # Esta função será chamada pelo FastAPI em um thread diferente.
        # Ela cria uma NOVA sessão para cada requisição, mas essa sessão
        # está vinculada à conexão transacional do teste.
        session = TestingSessionLocal()
        yield session
        session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Limpa o override após o teste ter sido concluído
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser", email="test@example.com", hashed_password=hashed_password
    )
    db_session.add(user)
    # Usamos flush para enviar a alteração para o DB dentro da transação atual
    db_session.flush()
    return user


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    login_data = {"username": test_user.username, "password": "testpassword"}
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == 200, f"Failed to get token: {response.json()}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
