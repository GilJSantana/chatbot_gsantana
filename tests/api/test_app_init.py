from fastapi.testclient import TestClient


def test_openapi_docs(client: TestClient):
    """Verifica se a documentação OpenAPI (Swagger) é gerada corretamente."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()


def test_routes_are_found_using_test_client(client: TestClient):
    """
    Verifica se as rotas são registradas e se o endpoint é executado,
    usando o cliente de teste que utiliza o banco de dados em memória.
    """
    login_data = {"username": "testuser", "password": "testpassword"}

    # A chamada agora usa o banco de dados em memória (fornecido pela fixture `client`).
    # Como o usuário não existe neste banco de dados de teste temporário,
    # esperamos um erro 401 Unauthorized.
    # Isso prova que a rota foi encontrada e que a lógica do endpoint foi
    # executada corretamente contra o banco de dados de teste.
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == 401
