

from fastapi import APIRouter

from .auth import router as auth_router
from .server import router as server_router
from .ticket import router as ticket_router
from .transaction import router as transaction_router
from .user import router as user_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(server_router)
router.include_router(ticket_router)
router.include_router(transaction_router)
router.include_router(user_router)
