from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.api import api_router
from .core.config import settings
# CORREÇÃO: Importa o módulo database inteiro para garantir que o monkeypatch funcione.
from .core import database as database_module


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida para inicializar recursos na inicialização
    e limpá-los no encerramento.
    """
    # CORREÇÃO: Usa o engine a partir do módulo para que ele possa ser substituído nos testes.
    database_module.Base.metadata.create_all(bind=database_module.engine)
    yield
    # Adicione aqui código para limpeza no encerramento, se necessário.


app = FastAPI(
    title="Chatbot LabYes",
    description="API para o chatbot de FAQ do LabYes",
    version="0.1.0",
    lifespan=lifespan,
)

# --- Configuração do CORS ---
origins = [
    "http://localhost",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusão dos Roteadores ---
# O prefixo da API é definido diretamente para evitar o erro de configuração nos testes.
app.include_router(api_router, prefix="/api/v1")


@app.get("/health-check")
def health_check():
    """Endpoint simples para verificar a saúde da aplicação."""
    return {"status": "ok"}
