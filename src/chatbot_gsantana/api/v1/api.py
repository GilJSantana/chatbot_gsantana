from fastapi import APIRouter

from .endpoints import chat, faq, login

api_router = APIRouter()

# Inclui os roteadores para cada parte da API
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(faq.router, prefix="/faqs", tags=["FAQs"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
