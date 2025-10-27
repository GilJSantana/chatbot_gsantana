import logging
from fastapi.testclient import TestClient


def test_logging_middleware_success(client: TestClient, caplog):
    """
    Testa se o middleware de logging registra corretamente uma requisição bem-sucedida.
    """
    # Define o nível de captura do log para INFO
    with caplog.at_level(logging.INFO):
        # Faz uma requisição para um endpoint qualquer
        response = client.get("/health-check")
        assert response.status_code == 200

    # Verifica se algum log foi capturado
    assert len(caplog.records) > 0, "Nenhum log foi capturado."

    # Procura pelo log do evento 'request_finished'
    found_log_record = None
    for record in caplog.records:
        # O structlog anexa o dicionário de log ao atributo 'msg' do registro
        if (
            isinstance(record.msg, dict)
            and record.msg.get("event") == "request_finished"
        ):
            found_log_record = record
            break

    # Garante que o registro de log foi encontrado
    assert (
        found_log_record is not None
    ), "O registro de log 'request_finished' não foi encontrado."

    # Agora, fazemos as asserções diretamente no dicionário do log
    log_data = found_log_record.msg
    assert log_data["level"] == "info"
    assert log_data["path"] == "/health-check"
    assert log_data["method"] == "GET"
    assert log_data["status_code"] == 200
    assert "process_time" in log_data
