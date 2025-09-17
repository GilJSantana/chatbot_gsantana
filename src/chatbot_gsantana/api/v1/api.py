from fastapi import APIRouter

from .endpoints import faq

api_router = APIRouter()
api_router.include_router(faq.router, prefix="/faqs", tags=["FAQs"])
