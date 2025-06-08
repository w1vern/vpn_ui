

from .auth import AuthController
from .server import ServerController
from .ticket import TicketController
from .transaction import TransactionController
from .user import UserController
from fastapi import APIRouter

router = APIRouter(prefix="/api")
router.include_router(AuthController.create_router())
router.include_router(ServerController.create_router())
router.include_router(TicketController.create_router())
router.include_router(ServerController.create_router())
router.include_router(TransactionController.create_router())
router.include_router(UserController.create_router())