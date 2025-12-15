import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "invalid_data",
    [
        ({"question": "", "answer": "Uma resposta válida."}),
        ({"question": "Uma pergunta válida.", "answer": ""}),
        ({"answer": "Faltando a pergunta."}),
        ({"question": "Faltando a resposta."}),
        ({"question": 123, "answer": "Tipo de dado incorreto para pergunta."}),
        ({"question": "Tipo de dado incorreto para resposta.", "answer": 123}),
    ],
)
def test_create_faq_with_invalid_data_fails(
    client: TestClient, admin_auth_headers: dict, invalid_data: dict
):
    """
    Verifica se a criação de uma FAQ com dados inválidos falha.
    Exemplos: campos em branco, ausentes ou com tipos de dados incorretos.
    Deve retornar 422 Unprocessable Entity.
    """
    response = client.post(
        "/api/v1/faqs/", json=invalid_data, headers=admin_auth_headers
    )
    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_data",
    [
        ({"question": "", "answer": "Uma resposta válida."}),
        ({"question": "Uma pergunta válida.", "answer": ""}),
        ({"question": 123, "answer": "Tipo de dado incorreto para pergunta."}),
        ({"question": "Tipo de dado incorreto para resposta.", "answer": 123}),
    ],
)
def test_update_faq_with_invalid_data_fails(
    client: TestClient, admin_auth_headers: dict, invalid_data: dict
):
    """
    Verifica se a atualização de uma FAQ com dados inválidos falha.
    Exemplos: campos em branco ou com tipos de dados incorretos.
    Deve retornar 422 Unprocessable Entity.
    """
    # Primeiro, cria uma FAQ para depois tentar atualizar
    faq_data = {"question": "Pergunta original", "answer": "Resposta original"}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    assert response.status_code == 201
    faq_id = response.json()["id"]

    # Agora, tenta atualizar a FAQ com dados inválidos
    response = client.put(
        f"/api/v1/faqs/{faq_id}", json=invalid_data, headers=admin_auth_headers
    )
    assert response.status_code == 422


def test_delete_faq_as_admin_succeeds(client: TestClient, admin_auth_headers: dict):
    """
    Verifica se um administrador pode deletar uma FAQ.
    Deve retornar 200 OK.
    """
    # Cria uma FAQ para deletar
    faq_data = {"question": "FAQ para deletar", "answer": "..."}
    response = client.post("/api/v1/faqs/", json=faq_data, headers=admin_auth_headers)
    assert response.status_code == 201
    faq_id = response.json()["id"]

    # Deleta a FAQ
    response = client.delete(f"/api/v1/faqs/{faq_id}", headers=admin_auth_headers)
    assert response.status_code == 200

    # Verifica se a FAQ foi realmente deletada
    response = client.get(f"/api/v1/faqs/{faq_id}", headers=admin_auth_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "FAQ not found"}
