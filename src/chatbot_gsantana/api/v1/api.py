from fastapi import APIRouter

from .endpoints import chat, faq, login, users

api_router = APIRouter()
# Inclui os roteadores dos endpoints no roteador principal da API.
# Os prefixos aqui são relativos ao prefixo do api_router em main.py (/api/v1).
api_router.include_router(login.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(faq.router, prefix="/faqs", tags=["FAQs"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
