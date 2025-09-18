from fastapi import FastAPI

from .api.v1.api import api_router
from .core.database import Base, engine

# Cria as tabelas no banco de dados (para desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Chatbot LabYes",
    description="API para o chatbot de FAQ do LabYes",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health-check")
def health_check():
    """Verifica se a aplicação está funcionando."""
    return {"status": "ok"}
