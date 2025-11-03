import pytest
from playwright.sync_api import Page, expect, APIRequestContext

pytestmark = pytest.mark.e2e

def setup_test_faq(api_request_context: APIRequestContext, admin_auth_headers: dict):
    """Helper para garantir que a FAQ de teste exista, usando URLs relativas."""
    # Tenta deletar primeiro para garantir um estado limpo. 
    # A ausência do fail_on_status=False é intencional; a chamada prossegue mesmo com 404.
    api_request_context.delete("/api/v1/faqs/by_question/Olá", headers=admin_auth_headers)

    # Cria a FAQ de teste
    response = api_request_context.post(
        "/api/v1/faqs/",
        headers=admin_auth_headers,
        data={"question": "Olá", "answer": "Olá! Como posso ajudar?"}
    )
    assert response.ok


def test_full_onboarding_and_faq_flow(page: Page, api_request_context: APIRequestContext, admin_auth_headers: dict):
    """Testa o fluxo completo, desde o onboarding até a interação com a FAQ."""
    setup_test_faq(api_request_context, admin_auth_headers)

    # A `base_url` é injetada automaticamente pelo Playwright no `page.goto()`
    page.goto("/")
    page.evaluate("localStorage.clear()")
    page.reload()

    chat_icon = page.locator("#chatbotIconContainer")
    expect(chat_icon).to_be_visible()
    chat_icon.click()

    chat_body = page.locator("#chatBody")
    expect(chat_body.get_by_text("qual é o seu nome?")).to_be_visible()

    def respond_to_chat(message: str):
        page.locator("#chatInput").fill(message)
        page.locator("#sendMessage").click()

    respond_to_chat("Usuário de Teste E2E")
    expect(chat_body.get_by_text("Quais são seus conhecimentos?")).to_be_visible()

    respond_to_chat("Playwright, Pytest, Docker")
    expect(chat_body.get_by_text("Onde você mora?")).to_be_visible()

    respond_to_chat("Ambiente de Teste")
    expect(chat_body.get_by_text("quais são seus hobbies?")).to_be_visible()

    respond_to_chat("Automatizar testes")
    expect(chat_body.get_by_text("Tudo certo! Seu perfil foi salvo.")).to_be_visible()

    respond_to_chat("Olá")
    expect(chat_body.get_by_text("Olá! Como posso ajudar?")).to_be_visible()
