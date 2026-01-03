
from fastapi import APIRouter, Cookie, Depends

from ..config import SECURE_COOKIES, Config
from ..response import SuccessResponse
from ..schemas import TgAuth, TgId
from ..services import AuthService, UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/refresh",
    summary="Refresh the access token"
)
async def refresh(
    refresh_token: str | None = Cookie(None),
    auth_service: AuthService = Depends(AuthService.depends)
) -> SuccessResponse:
    response = SuccessResponse()
    access = await auth_service.refresh(refresh_token)
    response.set_cookie(
        key="access_token",
        value=access,
        max_age=Config.access_token_lifetime,
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api"
    )
    return response


@router.post(
    path="/login",
    summary="Login using Telegram authentication"
)
async def login(
    tg_auth: TgAuth,
    auth_service: AuthService = Depends(AuthService.depends)
) -> SuccessResponse:
    refresh, access = await auth_service.login(tg_auth)
    response = SuccessResponse()
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        max_age=Config.refresh_token_lifetime,
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api/auth/refresh"
    )
    response.set_cookie(
        key="access_token",
        value=access,
        max_age=Config.access_token_lifetime,
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api"
    )
    return response


@router.post(
    path="/logout",
    summary="Logout the user"
)
async def logout() -> SuccessResponse:
    response = SuccessResponse()
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api/auth/refresh"
    )
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api"
    )
    return response


@router.post(
    path="/logout_all",
    summary="Logout the user from all devices"
)
async def logout_all(
    user_service: UserService = Depends(UserService.depends)
) -> SuccessResponse:
    await user_service.logout_all()
    response = SuccessResponse()
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api/auth/refresh"
    )
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite='strict',
        secure=SECURE_COOKIES,
        path="/api"
    )
    return response


@router.post(
    path="/tg_code",
    summary="Send a Telegram login code"
)
async def tg_code(
    tg_id: TgId,
    auth_service: AuthService = Depends(AuthService.depends)
) -> SuccessResponse:
    await auth_service.send_code(tg_id)
    return SuccessResponse()
