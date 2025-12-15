from fastapi.testclient import TestClient


def test_create_faq_as_admin_succeeds(client: TestClient, admin_auth_headers: dict):
    """
    Verifica se um administrador pode criar uma nova FAQ.
    Deve retornar 201 Created.
    """
    faq_data = {
        "question": "Qual é o horário de funcionamento?",
        "answer": "Das 9h às 18h.",
    }
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == faq_data["question"]
    assert data["answer"] == faq_data["answer"]


def test_create_faq_as_common_user_fails(
    client: TestClient, common_user_auth_headers: dict
):
    """
    Verifica se um usuário comum NÃO pode criar uma nova FAQ.
    Deve retornar 403 Forbidden.
    """
    faq_data = {"question": "Posso trazer meu pet?", "answer": "Não."}
    response = client.post(
        "/api/v1/faqs/", json=faq_data, headers=common_user_auth_headers
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}


def test_create_faq_unauthenticated_fails(client: TestClient):
    """
    Verifica se um acesso não autenticado NÃO pode criar uma nova FAQ.
    Deve retornar 401 Unauthorized.
    """
    faq_data = {"question": "Qual o valor do ingresso?", "answer": "R$ 50,00."}
    response = client.post("/api/v1/faqs/", json=faq_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_update_faq_as_admin_succeeds(client: TestClient, admin_auth_headers: dict):
    """
    Verifica se um administrador pode atualizar uma FAQ existente.
    Deve retornar 200 OK.
    """
    # Primeiro, cria uma FAQ para depois atualizar
    faq_data = {"question": "Pergunta original", "answer": "Resposta original"}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    assert response.status_code == 201
    faq_id = response.json()["id"]

    # Agora, atualiza a FAQ
    updated_data = {"question": "Pergunta atualizada", "answer": "Resposta atualizada"}
    response = client.put(
        f"/api/v1/faqs/{faq_id}", json=updated_data, headers=admin_auth_headers
    )
    assert response.status_code == 200
    assert response.json()["question"] == updated_data["question"]


def test_update_faq_as_common_user_fails(
    client: TestClient, admin_auth_headers: dict, common_user_auth_headers: dict
):
    """
    Verifica se um usuário comum NÃO pode atualizar uma FAQ.
    Deve retornar 403 Forbidden.
    """
    # Admin cria a FAQ
    faq_data = {"question": "FAQ para teste de update", "answer": "..."}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    faq_id = response.json()["id"]

    # Usuário comum tenta atualizar
    updated_data = {"question": "Tentativa de update", "answer": "Falha"}
    response = client.put(
        f"/api/v1/faqs/{faq_id}", json=updated_data, headers=common_user_auth_headers
    )
    assert response.status_code == 403


def test_delete_faq_as_admin_succeeds(client: TestClient, admin_auth_headers: dict):
    """
    Verifica se um administrador pode deletar uma FAQ.
    Deve retornar 204 No Content.
    """
    # Cria uma FAQ para deletar
    faq_data = {"question": "FAQ para deletar", "answer": "..."}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    faq_id = response.json()["id"]

    # Deleta a FAQ
    response = client.delete(f"/api/v1/faqs/{faq_id}", headers=admin_auth_headers)
    assert response.status_code == 200


def test_delete_faq_unauthenticated_fails(client: TestClient, admin_auth_headers: dict):
    """
    Verifica se um acesso não autenticado NÃO pode deletar uma FAQ.
    Deve retornar 401 Unauthorized.
    """
    faq_data = {"question": "FAQ para teste de delete", "answer": "..."}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    faq_id = response.json()["id"]

    response = client.delete(f"/api/v1/faqs/{faq_id}")
    assert response.status_code == 401
