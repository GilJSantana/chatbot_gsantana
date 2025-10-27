import time
import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Pega uma instância do logger configurado
log = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logar informações sobre cada requisição, incluindo
    o tempo de processamento e o status da resposta.
    """

    async def dispatch(self, request: Request, call_next):
        # Limpa o contexto de log para cada nova requisição
        structlog.contextvars.clear_contextvars()

        # Adiciona informações da requisição ao contexto do log
        structlog.contextvars.bind_contextvars(
            path=request.url.path,
            method=request.method,
            client_host=request.client.host,
        )

        start_time = time.time()

        try:
            # Processa a requisição
            response = await call_next(request)
            process_time = time.time() - start_time

            # Adiciona informações da resposta ao contexto
            structlog.contextvars.bind_contextvars(status_code=response.status_code)

            # Loga a finalização da requisição
            log.info(
                "request_finished",
                message="Requisição finalizada",
                process_time=round(process_time, 4),
            )

        except Exception as e:
            # Loga qualquer exceção não tratada
            log.exception(
                "unhandled_exception", message="Erro não tratado na aplicação"
            )
            # Re-levanta a exceção para que o FastAPI possa lidar com ela
            raise e

        return response
