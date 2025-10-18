from typing import Optional

from pydantic import BaseModel, ConfigDict


# --- Schemas Base ---
class FAQBase(BaseModel):
    """Schema base para FAQ, com campos comuns."""

    question: Optional[str] = None
    answer: Optional[str] = None


# --- Schema para Criação ---
class FAQCreate(FAQBase):
    """Schema usado para criar uma nova FAQ."""

    question: str
    answer: str


# --- Schema para Atualização ---
class FAQUpdate(FAQBase):
    """Schema usado para atualizar uma FAQ. Todos os campos são opcionais."""

    pass


# --- Schema para Leitura (Resposta da API) ---
class FAQ(FAQBase):
    """Schema usado para retornar uma FAQ da API."""

    id: int
    question: str
    answer: str

    # CORREÇÃO: Substitui a 'class Config' obsoleta pela nova 'model_config'
    model_config = ConfigDict(from_attributes=True)
