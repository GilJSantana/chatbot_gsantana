from fastapi import APIRouter

from .endpoints import faq, chat # Adicionado 'chat'

api_router = APIRouter()
api_router.include_router(faq.router, prefix="/faqs", tags=["FAQs"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"]) # Novo roteador para o chat
