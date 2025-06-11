
import random
from datetime import UTC, datetime

from fastapi import (APIRouter, Cookie, Depends, HTTPException, Request,
                     Response)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (RedisType, UserRepository, get_redis_client,
                             session_manager)

from ..broker import get_broker, send_message
from ..config import Config
from ..get_auth import get_user
from ..schemas import TgAuth, TgId, UserSchema
from ..token import AccessToken, RefreshToken


def create_code() -> str:
    tmp_code = str(random.randrange(start=0, stop=1000000))
    return "0"*(6-len(tmp_code)) + tmp_code


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/refresh",
    summary="Refresh the access token"
)
async def refresh(response: Response,
                  session: AsyncSession = Depends(session_manager.session),
                  refresh_token: str = Cookie(None)
                  ):
    if refresh_token is None:
        raise HTTPException(
            status_code=401, detail="refresh token doesn't exist")
    refresh = RefreshToken.from_token(refresh_token)
    current_time = datetime.now(UTC).replace(tzinfo=None)
    if refresh.created_date > current_time or refresh.created_date + refresh.lifetime < current_time:
        raise HTTPException(
            status_code=401, detail="refresh token expired")
    ur = UserRepository(session)
    user = await ur.get_by_id(refresh.user_id)
    if user is None:
        raise HTTPException(
            status_code=401, detail="incorrect refresh token")
    if user.secret != refresh.secret:
        raise HTTPException(
            status_code=401, detail="incorrect refresh token")
    access = AccessToken(user, current_time)
    response.set_cookie(key="access_token", value=access.to_token(
    ), max_age=Config.access_token_lifetime, httponly=True)
    return {"message": "OK"}


@router.post(
    path="/login",
    summary="Login using Telegram authentication"
)
async def login(request: Request,
                response: Response,
                tg_auth: TgAuth,
                redis: Redis = Depends(get_redis_client),
                session: AsyncSession = Depends(session_manager.session)
                ):
    lock_time = await redis.ttl(
        f"{RedisType.invalidated_access_token}:{tg_auth.tg_id}")
    if lock_time > 0:
        raise HTTPException(
            status_code=401, detail=f"login locked for {lock_time} seconds")
    ip = request.client.host  # type: ignore
    ip_counter = await redis.get(f"{RedisType.incorrect_credentials_ip}:{ip}")
    if ip_counter is not None:
        if int(ip_counter) >= Config.ip_buffer:
            raise HTTPException(
                status_code=401, detail=f"too many incorrect credentials for ip: {ip}")
    else:
        ip_counter = 0
    tg_code = await redis.get(f"{RedisType.tg_code}:{tg_auth.tg_id}")
    if tg_code is None:
        await redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}",
                        int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
        raise HTTPException(
            status_code=401, detail="code for user doesn't exist")
    ur = UserRepository(session)
    user = await ur.get_by_telegram_id(tg_auth.tg_id)
    if user is None:
        await redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}",
                        int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
        raise HTTPException(status_code=401, detail="user not found")
    if tg_auth.tg_code != tg_code:
        await redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}",
                        int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
        await redis.set(f"{RedisType.incorrect_credentials}:{user.id}",
                        0, ex=Config.login_gap)
        raise HTTPException(status_code=401, detail="invalid credentials")
    await redis.delete(f"{RedisType.tg_code}:{tg_auth.tg_id}")
    refresh = RefreshToken(user_id=user.id, secret=user.secret)
    access = AccessToken(user)
    response.set_cookie(key="refresh_token", value=refresh.to_token(
    ), max_age=Config.refresh_token_lifetime, httponly=True)
    response.set_cookie(key="access_token", value=access.to_token(
    ), max_age=Config.access_token_lifetime, httponly=True)
    return {"message": "OK"}


@router.post(
    path="/logout",
    summary="Logout the user"
)
async def logout(response: Response,
                 refresh_token: str = Cookie(None)
                 ):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="unauthorized")
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="access_token")
    return {"message": "OK"}


@router.post(
    path="/tg_code",
    summary="Send a Telegram login code"
)
async def tg_code(request: Request,
                  tg_id: TgId, broker=Depends(get_broker),
                  redis: Redis = Depends(get_redis_client),
                  session: AsyncSession = Depends(session_manager.session)
                  ):
    ip = request.client.host  # type: ignore
    ip_counter = await redis.get(f"{RedisType.incorrect_credentials_ip}:{ip}")
    if ip_counter is not None:
        if int(ip_counter) >= Config.ip_buffer:
            raise HTTPException(
                status_code=401, detail=f"too many incorrect credentials for ip: {ip}")
    else:
        ip_counter = 0
    ur = UserRepository(session)
    user = await ur.get_by_telegram_id(tg_id.tg_id)
    if user is None:
        await redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}",
                        int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
        raise HTTPException(status_code=401, detail="user not found")
    tg_code_time = await redis.ttl(f"{RedisType.tg_code}:{user.telegram_id}")
    gap = Config.tg_code_gap - Config.tg_code_lifetime + tg_code_time
    if tg_code_time > 0 and gap > 0:
        await redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}",
                        int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
        raise HTTPException(
            status_code=401, detail=f"new code could be sent in {gap} seconds")
    tg_code = create_code()
    await redis.set(f"{RedisType.tg_code}:{user.telegram_id}",
                    tg_code, ex=Config.tg_code_lifetime)
    await send_message({"tg_id": tg_id.tg_id, "text": "your code to login: " + tg_code}, broker)
    return {"message": "OK"}
