import os
import pytest
from playwright.sync_api import Playwright, APIRequestContext


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright, base_url: str) -> APIRequestContext:
    """
    Cria um contexto de requisição de API configurado com a base_url.
    Isso permite o uso de URLs relativas nas chamadas de API.
    """
    if not base_url:
        pytest.fail(
            "A `base_url` do Playwright " "não está definida. Execute com `--base-url`."
        )

    return playwright.request.new_context(base_url=base_url)


@pytest.fixture(scope="session")
def admin_auth_headers(api_request_context: APIRequestContext) -> dict:
    """Obtém um token de autenticação para o usuário admin de teste."""
    username = os.getenv("TEST_ADMIN_USERNAME", "admin_e2e")
    password = os.getenv("TEST_ADMIN_PASSWORD", "strong_test_password")

    # Agora usando uma URL relativa, pois o contexto já tem a base_url
    response = api_request_context.post(
        "/api/v1/auth/token", form={"username": username, "password": password}
    )

    assert response.ok, (
        f"Falha ao obter token de admin: " f"{response.status_text} - {response.json()}"
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
