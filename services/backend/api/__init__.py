

from fastapi import APIRouter

from .auth import router as auth_router
from .notifications import router as notifications_router
from .server import router as servers_router
from .tariff import router as tariffs_router
from .ticket import router as tickets_router
from .transaction import router as transactions_router
from .user import router as users_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(servers_router)
router.include_router(tickets_router)
router.include_router(transactions_router)
router.include_router(users_router)
router.include_router(tariffs_router)
router.include_router(notifications_router)
