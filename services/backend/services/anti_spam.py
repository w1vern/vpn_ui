
from fastapi import (
    Depends,
    Request,
)
from redis.asyncio import Redis

from ..config import Config
from ..exceptions import (
    LoginLockedException,
    RequestClientException,
    TooManyAttemptsFromIPException,
    TooSoonToSendCodeException,
)
from ..redis import (
    RedisType,
    get_redis_client,
)


class AntiSpamService:
    def __init__(self,
                 ip: str,
                 redis: Redis
                 ) -> None:
        self.redis = redis
        self.ip = ip

    @classmethod
    def depends(cls,
                request: Request,
                redis: Redis = Depends(get_redis_client)
                ) -> 'AntiSpamService':
        if request.client is None:
            raise RequestClientException()
        return cls(request.client.host, redis)

    async def increment_ip_attempts(self) -> None:
        key = f"{RedisType.incorrect_credentials_ip}:{self.ip}"
        value = await self.redis.get(key)
        counter = int(value) if value else 0
        counter += 1
        await self.redis.set(key, counter, ex=Config.ip_buffer_lifetime)
        if counter >= Config.ip_buffer:
            raise TooManyAttemptsFromIPException(self.ip)

    async def check_login_lock(self,
                               tg_id: int
                               ) -> None:
        key = f"{RedisType.invalidated_access_token}:{tg_id}"
        ttl = await self.redis.ttl(key)
        if ttl > 0:
            raise LoginLockedException(ttl)

    async def check_tg_code_gap(self,
                                tg_id: int
                                ) -> None:
        key = f"{RedisType.tg_code}:{tg_id}"
        ttl = await self.redis.ttl(key)
        if ttl > 0:
            gap = Config.tg_code_gap - Config.tg_code_lifetime + ttl
            if gap > 0:
                raise TooSoonToSendCodeException(gap)
