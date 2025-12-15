from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# --- Schemas Base ---
class FAQBase(BaseModel):
    """Schema base para FAQ, com campos comuns."""

    question: str
    answer: str


# --- Schema para Criação ---
class FAQCreate(FAQBase):
    """Schema usado para criar uma nova FAQ."""

    question: str = Field(
        ..., min_length=1, description="A pergunta não pode estar em branco."
    )
    answer: str = Field(
        ..., min_length=1, description="A resposta não pode estar em branco."
    )


# --- Schema para Atualização ---
class FAQUpdate(BaseModel):
    """Schema usado para atualizar uma FAQ. Todos os campos são opcionais."""

    question: Optional[str] = Field(
        None, min_length=1, description="A pergunta não pode estar em branco."
    )
    answer: Optional[str] = Field(
        None, min_length=1, description="A resposta não pode estar em branco."
    )


# --- Schema para Leitura (Resposta da API) ---
class FAQ(FAQBase):
    """Schema usado para retornar uma FAQ da API."""

    id: int

    # CORREÇÃO: Substitui a 'class Config' obsoleta pela nova 'model_config'
    model_config = ConfigDict(from_attributes=True)
