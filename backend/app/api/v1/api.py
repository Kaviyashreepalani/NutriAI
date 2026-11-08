from fastapi import APIRouter
from app.api.v1.public import router as public_router
from app.api.v1.auth import router as auth_router
from app.api.v1.profile import router as profile_router
from app.api.v1.reports import router as reports_router
from app.api.v1.assessments import router as assessments_router
from app.api.v1.formulations import router as formulations_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.shop import router as shop_router
from app.api.v1.cart import router as cart_router
from app.api.v1.checkout import router as checkout_router
from app.api.v1.orders import router as orders_router
from app.api.v1.progress import router as progress_router
from app.api.v1.history import router as history_router
from app.api.v1.chat import router as chat_router
from app.api.v1.voice import router as voice_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(public_router)
api_router.include_router(auth_router)
api_router.include_router(profile_router)
api_router.include_router(reports_router)
api_router.include_router(assessments_router)
api_router.include_router(formulations_router)
api_router.include_router(recommendations_router)
api_router.include_router(shop_router)
api_router.include_router(cart_router)
api_router.include_router(checkout_router)
api_router.include_router(orders_router)
api_router.include_router(progress_router)
api_router.include_router(history_router)
api_router.include_router(chat_router)
api_router.include_router(voice_router)
api_router.include_router(admin_router)

