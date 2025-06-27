
import random
from datetime import UTC, datetime

from fastapi import Depends
from faststream.rabbit import RabbitBroker
from redis.asyncio import Redis

from shared.database import UserRepository
from shared.infrastructure import (
    CodeToTG,
    RedisType,
    get_redis_client,
)

from ..config import Config
from ..exceptions import (
    CodeNotFoundException,
    InvalidCredentialsException,
    RefreshTokenExpiredException,
    RefreshTokenInvalidException,
    RefreshTokenMissingException,
    UserNotFoundException,
)
from ..rabbit import get_broker, send_tg_code
from ..schemas import TgAuth, TgId
from ..token import AccessToken, RefreshToken
from .anti_spam import AntiSpamService
from .depends import get_user_repo


class AuthService:
    def __init__(self,
                 ur: UserRepository,
                 redis: Redis,
                 broker: RabbitBroker,
                 anti_spam: AntiSpamService):
        self.ur = ur
        self.redis = redis
        self.broker = broker
        self.anti_spam = anti_spam

    @classmethod
    def depends(cls,
                ur: UserRepository = Depends(get_user_repo),
                redis: Redis = Depends(get_redis_client),
                broker: RabbitBroker = Depends(get_broker),
                anti_spam: AntiSpamService = Depends(AntiSpamService.depends)
                ) -> 'AuthService':
        return cls(ur, redis, broker, anti_spam)

    async def _create_code(self) -> str:
        return f"{random.randint(0, 999999):06}"

    async def login(self,
                    tg_auth: TgAuth
                    ) -> tuple[str, str]:

        await self.anti_spam.increment_ip_attempts()
        await self.anti_spam.check_login_lock(tg_auth.tg_id)

        tg_code = await self.redis.get(f"{RedisType.tg_code}:{tg_auth.tg_id}")
        if tg_code is None:
            raise CodeNotFoundException()

        user = await self.ur.get_by_telegram_id(tg_auth.tg_id)
        if user is None:
            raise UserNotFoundException()

        if tg_auth.tg_code != tg_code:
            await self.redis.set(f"{RedisType.incorrect_credentials}:{tg_auth.tg_id}", 0,
                                 ex=Config.login_gap)
            raise InvalidCredentialsException()

        await self.redis.delete(f"{RedisType.tg_code}:{user.telegram_id}")

        refresh = RefreshToken(user_id=user.id, secret=user.secret).to_token()
        access = AccessToken(user).to_token()

        return refresh, access

    async def refresh(self,
                      refresh_token: str | None,
                      ) -> str:
        if refresh_token is None:
            raise RefreshTokenMissingException()

        refresh = RefreshToken.from_token(refresh_token)
        now = datetime.now(UTC).replace(tzinfo=None)

        if refresh.created_date > now or refresh.created_date + refresh.lifetime < now:
            raise RefreshTokenExpiredException()

        user = await self.ur.get_by_id(refresh.user_id)
        if not user or user.secret != refresh.secret:
            raise RefreshTokenInvalidException()

        access = AccessToken(user, now).to_token()
        return access
        
        

    async def send_code(self,
                        tg_id: TgId,
                        ) -> None:
        await self.anti_spam.increment_ip_attempts()

        user = await self.ur.get_by_telegram_id(tg_id.tg_id)
        if user is None:
            raise UserNotFoundException()

        await self.anti_spam.check_tg_code_gap(user.telegram_id)

        code = await self._create_code()
        await self.redis.set(f"{RedisType.tg_code}:{user.telegram_id}",
                             code, ex=Config.tg_code_lifetime)

        await send_tg_code(CodeToTG(tg_id=user.telegram_id,
                                    code=code),
                           self.broker)
