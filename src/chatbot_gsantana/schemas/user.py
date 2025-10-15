from typing import List

from pydantic import BaseModel, EmailStr
from .faq import FAQ


class UserBase(BaseModel):
    """Schema base para o usuário."""

    username: str
    email: EmailStr  # Adiciona o campo email com validação de formato


class UserCreate(UserBase):
    """Schema para a criação de um novo usuário."""

    password: str


class User(UserBase):
    """Schema para a leitura de um usuário."""

    id: int
    is_active: bool = True
    faqs: List[FAQ] = []

    class Config:
        from_attributes = True
