

from fastapi import APIRouter
from back.api.auth import AuthController
from back.api.server import ServerController


router = APIRouter(prefix="/api")
router.include_router(AuthController.create_router())
router.include_router(ServerController.create_router())