
import random
from datetime import UTC, datetime

from fastapi import Cookie, Depends, HTTPException, Request, Response
from fastapi_controllers import Controller, get, post
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from back.broker import get_broker, send_message
from back.config import Config
from back.get_auth import get_user
from back.schemas import tg
from back.schemas.tg import TgAuth, TgId
from back.schemas.user import UserRightsSchema, UserSchema, UserSettingsSchema
from back.token import AccessToken, RefreshToken
from infra.database.main import get_db_session
from infra.database.models.user import User
from infra.database.redis import RedisType, get_redis_client
from infra.database.repositories.user_repository import UserRepository


def create_code() -> str:
    tmp_code = str(random.randrange(start=0, stop=1000000))
    return "0"*(6-len(tmp_code)) + tmp_code


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @post("/refresh",
          summary="Refresh the access token",
          description=(
              "This endpoint refreshes the access token (`access_token`) using the provided "
              "`refresh_token`. If the `refresh_token` is missing, expired, or invalid, "
              "it returns a 401 Unauthorized error."
          ),
          responses={
              200: {
                  "description": "Access token successfully refreshed",
                  "content": {
                      "application/json": {
                          "example": {"message": "OK"}
                      }
                  },
              },
              401: {"description": "Invalid or expired refresh token"},
          },)
    async def refresh(self, response: Response, session: AsyncSession = Depends(get_db_session), refresh_token: str = Cookie(None)):
        if refresh_token is None:
            raise HTTPException(
                status_code=401, detail="refresh token doesn't exist")
        refresh = RefreshToken.from_token(refresh_token)
        current_time = datetime.now(UTC).replace(tzinfo=None)
        if refresh.created_date > current_time or refresh.created_date + refresh.lifetime < current_time:
            raise HTTPException(
                status_code=401, detail="refresh token expired")
        ur = UserRepository(self.session)
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

    @post("/login",
          summary="Login using Telegram authentication",
          description=(
              "This endpoint authenticates the user using their Telegram credentials. "
              "It verifies the provided Telegram code (`tg_code`) and generates both "
              "`access_token` and `refresh_token`. These tokens are set as HTTP-only cookies."
          ),
          responses={
              200: {
                  "description": "User successfully authenticated",
                  "content": {
                      "application/json": {
                          "example": {"message": "OK"}
                      }
                  },
              },
              401: {
                  "description": (
                      "Authentication failed due to incorrect Telegram code, missing user, "
                      "or invalid credentials"
                  ),
              },
          },
          )
    async def login(self, request: Request, response: Response, tg_auth: TgAuth, redis=Depends(get_redis_client)):
        lock_time = redis.ttl(f"{RedisType.invalidated_access_token}:{tg_auth.tg_id}")
        if lock_time > 0:
            raise HTTPException(status_code=401, detail=f"login locked for {lock_time} seconds")
        ip = request.client.host #type: ignore
        ip_counter = redis.get(f"{RedisType.incorrect_credentials_ip}:{ip}")
        if ip_counter is not None:
             if int(ip_counter) >= Config.ip_buffer:
                  raise HTTPException(status_code=401, detail=f"too many incorrect credentials for ip: {ip}")
        else: ip_counter = 0
        tg_code = redis.get(f"{RedisType.tg_code}:{tg_auth.tg_id}")
        if tg_code is None:
            redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}", int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
            raise HTTPException(
                status_code=401, detail="code for user doesn't exist")
        tg_code = tg_code.decode("utf-8")
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(tg_auth.tg_id)
        if user is None:
            redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}", int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
            raise HTTPException(status_code=401, detail="user not found")
        if tg_auth.tg_code != tg_code:
            redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}", int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
            redis.set(f"{RedisType.incorrect_credentials}:{user.id}", 0, ex=Config.login_gap)
            raise HTTPException(status_code=401, detail="invalid credentials")
        redis.delete(f"{RedisType.tg_code}:{tg_auth.tg_id}")
        refresh = RefreshToken(user_id=user.id, secret=user.secret)
        access = AccessToken(user)
        response.set_cookie(key="refresh_token", value=refresh.to_token(
        ), max_age=Config.refresh_token_lifetime, httponly=True)
        response.set_cookie(key="access_token", value=access.to_token(
        ), max_age=Config.access_token_lifetime, httponly=True)
        return {"message": "OK"}

    @post(
        "/logout",
        summary="Logout the user",
        description=(
            "This endpoint logs out the user by deleting the `refresh_token` and `access_token` cookies. "
            "No authentication is required to call this endpoint."
        ),
        responses={
            200: {"description": "User successfully logged out"},
        },
    )
    async def logout(self, response: Response, refresh_token: str = Cookie(None)):
        if refresh_token is None:
            raise HTTPException(status_code=401, detail="unauthorized")
        response.delete_cookie(key="refresh_token")
        response.delete_cookie(key="access_token")
        return {"message": "OK"}

    @post(
        "/tg_code",
        summary="Send a Telegram login code",
        description=(
            "This endpoint generates a login code for the user associated with the provided Telegram ID. "
            "The code is stored in Redis with a time-to-live (TTL) and sent to the user's Telegram account."
        ),
        responses={
            200: {"description": "Code successfully generated and sent"},
            401: {"description": "User with the provided Telegram ID not found"},
        },
    )
    async def tg_code(self, request: Request, tg_id: TgId, broker=Depends(get_broker), redis=Depends(get_redis_client)):
        ip = request.client.host #type: ignore
        ip_counter = redis.get(f"{RedisType.incorrect_credentials_ip}:{ip}")
        if ip_counter is not None:
             if int(ip_counter) >= Config.ip_buffer:
                  raise HTTPException(status_code=401, detail=f"too many incorrect credentials for ip: {ip}")
        else: ip_counter = 0
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(tg_id.tg_id)
        if user is None:
            redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}", int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
            raise HTTPException(status_code=401, detail="user not found")
        tg_code_time = redis.ttl(f"{RedisType.tg_code}:{user.telegram_id}")
        gap = Config.tg_code_gap - Config.tg_code_lifetime + tg_code_time
        if tg_code_time > 0 and gap > 0:
            redis.set(f"{RedisType.incorrect_credentials_ip}:{ip}", int(ip_counter) + 1, ex=Config.ip_buffer_lifetime)
            raise HTTPException(status_code=401, detail=f"new code could be sent in {gap} seconds")
        tg_code = create_code()
        redis.set(f"{RedisType.tg_code}:{user.telegram_id}",
                  tg_code, ex=Config.tg_code_lifetime)
        await send_message({"tg_id": tg_id.tg_id, "text": "your code to login: " + tg_code}, broker)
        return {"message": "OK"}

    @get("/user_info", response_model=UserSchema)
    async def get_user_info(self, user: UserSchema = Depends(get_user)) -> UserSchema:
        return user
