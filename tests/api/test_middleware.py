import logging
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient


@patch("chatbot_gsantana.api.middleware.log")
def test_logging_middleware_success(mock_log: MagicMock, client: TestClient):
    """
    Testa se o middleware de logging chama o logger com os dados corretos.
    """
    response = client.get("/health-check")
    assert response.status_code == 200

    assert mock_log.info.called

    # Acessa a última chamada feita ao mock
    last_call = mock_log.info.call_args
    
    # O primeiro argumento posicional é o nome do evento
    event_name = last_call.args[0]
    # Os argumentos de palavra-chave são os metadados
    log_data = last_call.kwargs

    # Verifica o conteúdo do log
    assert event_name == "request_finished"
    assert log_data.get("message") == "Requisição finalizada"
    assert "process_time" in log_data
