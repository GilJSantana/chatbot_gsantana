from fastapi.testclient import TestClient


def test_create_faq(client: TestClient, auth_headers: dict):
    """Criação de FAQ com autenticação."""
    response = client.post(
        "/api/v1/faqs/",
        headers=auth_headers,
        json={
            "question": "Qual o horário de funcionamento?",
            "answer": "Das 8h às 18h.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == "Qual o horário de funcionamento?"
    assert data["answer"] == "Das 8h às 18h."


def test_read_faqs(client: TestClient, auth_headers: dict):
    """Listagem de FAQs após criação."""
    # Cria FAQ de teste
    client.post(
        "/api/v1/faqs/",
        headers=auth_headers,
        json={"question": "Qual horário?", "answer": "Das 8h às 18h."},
    )

    # CORREÇÃO DEFINITIVA: Adiciona os cabeçalhos de autenticação à chamada GET
    response = client.get("/api/v1/faqs/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(faq["question"] == "Qual horário?" for faq in data)


def test_create_faq_without_auth(client: TestClient):
    """Tentativa de criação de FAQ sem autenticação deve falhar."""
    response = client.post(
        "/api/v1/faqs/",
        json={"question": "Pergunta sem auth", "answer": "Resposta"},
    )
    assert response.status_code == 401
