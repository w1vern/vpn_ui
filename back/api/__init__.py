

from fastapi import APIRouter
from back.api.auth import AuthController


router = APIRouter(prefix="/api")
router.include_router(AuthController.create_router())