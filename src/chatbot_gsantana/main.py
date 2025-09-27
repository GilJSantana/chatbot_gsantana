from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.api import api_router
from .core.database import Base, engine

# Cria as tabelas no banco de dados (para desenvolvimento)
Base.metadata.create_all(bind=engine)

# De volta ao básico: Deixa o FastAPI gerenciar os URLs da documentação
app = FastAPI(
    title="Chatbot LabYes",
    description="API para o chatbot de FAQ do LabYes",
    version="0.1.0",
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
# --- Fim da Configuração do CORS ---

app.include_router(api_router, prefix="/api/v1")


@app.get("/health-check")
def health_check():
    """Verifica se a aplicação está funcionando."""
    return {"status": "ok"}
