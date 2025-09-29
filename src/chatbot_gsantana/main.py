from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.api import api_router


# --- Gerenciador de Ciclo de Vida da Aplicação ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Em um cenário de produção real, a criação de tabelas é geralmente
    # gerenciada por uma ferramenta de migração como Alembic.
    yield
    # Código a ser executado no encerramento (se necessário)


# --- Criação da Instância do App FastAPI ---
app = FastAPI(
    title="Chatbot LabYes",
    description="API para o chatbot de FAQ do LabYes",
    version="0.1.0",
    lifespan=lifespan,  # Usa o novo gerenciador de ciclo de vida
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
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# --- Inclusão dos Roteadores ---
app.include_router(api_router, prefix="/api/v1")


@app.get("/health-check")
def health_check():
    """Verifica se a aplicação está funcionando."""
    return {"status": "ok"}
