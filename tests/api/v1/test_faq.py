from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_faq_unauthenticated(client: TestClient):
    """
    Testa se a criação de FAQ falha sem autenticação.
    """
    response = client.post("/api/v1/faqs/", json={"question": "Q1", "answer": "A1"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_update_faq_unauthenticated(client: TestClient):
    """
    Testa se a atualização de FAQ falha sem autenticação.
    """
    response = client.put("/api/v1/faqs/1", json={"question": "Q1", "answer": "A1"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_delete_faq_unauthenticated(client: TestClient):
    """
    Testa se a exclusão de FAQ falha sem autenticação.
    """
    response = client.delete("/api/v1/faqs/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_read_faqs_authenticated(client: TestClient, admin_auth_headers: dict):
    """
    Testa se a leitura de FAQs funciona com autenticação.
    """
    response = client.get("/api/v1/faqs/", headers=admin_auth_headers)
    assert response.status_code == 200


def test_create_faq_authenticated(
    client: TestClient, db_session: Session, admin_auth_headers: dict
):
    """
    Testa se a criação de FAQ funciona com autenticação.
    """
    faq_data = {"question": "Qual o horário?", "answer": "Das 9h às 18h."}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["question"] == faq_data["question"]
    assert data["answer"] == faq_data["answer"]
    assert "id" in data


def test_read_faqs_after_creation(client: TestClient, admin_auth_headers: dict):
    """
    Testa a listagem de FAQs após a criação de uma.
    """
    # Cria uma FAQ de teste para garantir que a lista não esteja vazia
    client.post(
        "/api/v1/faqs/",
        headers=admin_auth_headers,
        json={"question": "Qual horário de funcionamento?", "answer": "Das 8h às 18h."},
    )

    # CORREÇÃO DEFINITIVA: Passa os cabeçalhos de autenticação para a chamada GET
    response = client.get("/api/v1/faqs/", headers=admin_auth_headers)

    assert response.status_code == 200
    # Garante que a resposta é uma lista e que contém pelo menos um item
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
