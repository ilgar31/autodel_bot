from aiogram import Router
from .start import router as start_router
from .dealers import router as dealers_router
from .promo import router as promo_router
from .dice import router as dice_router
from .contact import router as contact_router
from .chat import router as chat_router
from .common import router as common_router
from .broadcast import router as broadcast_router

router = Router()

# Подключаем все роутеры
router.include_router(start_router)
router.include_router(dealers_router)
router.include_router(promo_router)
router.include_router(dice_router)
router.include_router(contact_router)
router.include_router(chat_router)
router.include_router(broadcast_router)
router.include_router(common_router)
