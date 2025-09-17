from pydantic import BaseModel


class FAQBase(BaseModel):
    """Schema base para FAQ, com campos comuns."""

    question: str
    answer: str


class FAQCreate(FAQBase):
    """Schema para a criação de uma nova FAQ."""

    pass


class FAQ(FAQBase):
    """Schema para a leitura de uma FAQ, incluindo o ID."""

    id: int

    class Config:
        from_attributes = True
