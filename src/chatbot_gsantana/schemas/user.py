from pydantic import BaseModel


class UserBase(BaseModel):
    """Schema base para o usuário."""

    username: str


class UserCreate(UserBase):
    """Schema para a criação de um novo usuário."""

    password: str


class User(UserBase):
    """Schema para a leitura de um usuário."""

    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema para o token de acesso."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema para os dados contidos no token JWT."""

    username: str | None = None
