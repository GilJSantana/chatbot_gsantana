from fastapi.testclient import TestClient


def test_create_faq(client: TestClient):
    """Testa a criação de uma nova FAQ."""
    response = client.post(
        "/api/v1/faqs/",
        json={"question": "Qual o horário de funcionamento?", "answer": "Das 8h às 18h."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Qual o horário de funcionamento?"
    assert data["answer"] == "Das 8h às 18h."
    assert "id" in data


def test_read_faqs(client: TestClient):
    """Testa a listagem de FAQs."""
    client.post(
        "/api/v1/faqs/",
        json={"question": "Qual o horário?", "answer": "Das 8h às 18h."},
    )
    response = client.get("/api/v1/faqs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["question"] == "Qual o horário?"


def test_read_faq(client: TestClient):
    """Testa a busca de uma FAQ específica."""
    response = client.post(
        "/api/v1/faqs/",
        json={"question": "Qual o endereço?", "answer": "Rua Exemplo, 123."},
    )
    faq_id = response.json()["id"]

    response = client.get(f"/api/v1/faqs/{faq_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Qual o endereço?"
    assert data["id"] == faq_id


def test_read_faq_not_found(client: TestClient):
    """Testa a busca de uma FAQ que não existe."""
    response = client.get("/api/v1/faqs/999")
    assert response.status_code == 404


def test_update_faq(client: TestClient):
    """Testa a atualização de uma FAQ."""
    response = client.post(
        "/api/v1/faqs/",
        json={"question": "Qual o telefone?", "answer": "(11) 1234-5678"},
    )
    faq_id = response.json()["id"]

    response = client.put(
        f"/api/v1/faqs/{faq_id}",
        json={"question": "Qual o novo telefone?", "answer": "(11) 9999-8888"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Qual o novo telefone?"
    assert data["answer"] == "(11) 9999-8888"


def test_delete_faq(client: TestClient):
    """Testa a exclusão de uma FAQ."""
    response = client.post(
        "/api/v1/faqs/",
        json={
            "question": "Item a ser deletado",
            "answer": "Resposta a ser deletada",
        },
    )
    faq_id = response.json()["id"]

    response = client.delete(f"/api/v1/faqs/{faq_id}")
    assert response.status_code == 200

    # Verifica se foi realmente deletado
    response = client.get(f"/api/v1/faqs/{faq_id}")
    assert response.status_code == 404
