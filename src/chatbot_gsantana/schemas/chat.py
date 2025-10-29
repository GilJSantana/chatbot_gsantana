from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Schema para uma mensagem de chat recebida."""

    session_id: str
    message: str


class ChatResponse(BaseModel):
    """Schema para a resposta do chat."""

    reply: str
