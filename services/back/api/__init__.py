

from back.api.auth import AuthController
from back.api.server import ServerController
from back.api.ticket import TicketController
from fastapi import APIRouter

router = APIRouter(prefix="/api")
router.include_router(AuthController.create_router())
router.include_router(ServerController.create_router())
router.include_router(TicketController.create_router())
router.include_router(ServerController.create_router())