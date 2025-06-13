
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Response,
)

from ..response import SuccessResponse
from ..schemas import TgAuth, TgId
from ..services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/refresh",
    summary="Refresh the access token"
)
async def refresh(response: Response,
                  refresh_token: str | None = Cookie(None),
                  auth_service: AuthService = Depends(AuthService.depends)
                  ) -> SuccessResponse:
    await auth_service.refresh(refresh_token, response)
    return SuccessResponse()


@router.post(
    path="/login",
    summary="Login using Telegram authentication"
)
async def login(response: Response,
                tg_auth: TgAuth,
                auth_service: AuthService = Depends(AuthService.depends)
                ) -> SuccessResponse:
    await auth_service.login(tg_auth, response)
    return SuccessResponse()


@router.post(
    path="/logout",
    summary="Logout the user"
)
async def logout(response: Response,
                 auth_service: AuthService = Depends(AuthService.depends)
                 ) -> SuccessResponse:
    await auth_service.logout(response)
    return SuccessResponse()


@router.post(
    path="/tg_code",
    summary="Send a Telegram login code"
)
async def tg_code(tg_id: TgId,
                  auth_service: AuthService = Depends(AuthService.depends)
                  ) -> SuccessResponse:
    await auth_service.send_code(tg_id)
    return SuccessResponse()
