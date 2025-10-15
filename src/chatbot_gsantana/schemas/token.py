from pydantic import BaseModel


class Token(BaseModel):
    """Schema para o token de acesso."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema para os dados contidos no token JWT."""

    # O campo padrão para o "assunto" do token JWT é 'sub'.
    sub: str | None = None
