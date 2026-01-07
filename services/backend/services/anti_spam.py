
from fastapi import Depends, Request
from redis.asyncio import Redis

from ..config import Config
from ..exceptions import (
    LoginLockedException,
    RequestClientException,
    TooManyAttemptsFromIPException,
    TooSoonToSendCodeException
)
from ..redis import RedisType, get_redis_client


class AntiSpamService:
    def __init__(self,
                 ip: str,
                 redis: Redis
                 ) -> None:
        self.redis = redis
        self.ip = ip

    @classmethod
    def depends(
        cls,
        request: Request,
        redis: Redis = Depends(get_redis_client)
    ) -> 'AntiSpamService':
        ip = cls._get_client_ip(request)
        return cls(ip, redis)
    
    @staticmethod
    def _get_client_ip(request: Request) -> str:
        print(request.headers)
        forwarded_for = request.headers.get("X-Forwarded-For")
        print(forwarded_for)
        if forwarded_for:
            res = forwarded_for.split(",")[0].strip()
            print(res)
            return res
        real_ip = request.headers.get("X-Real-IP")
        print(real_ip)
        if real_ip:
            return real_ip.strip()
        if request.client is None:
            raise RequestClientException()
        print(request.client.host)
        return request.client.host

    async def increment_ip_attempts(self) -> None:
        key = f"{RedisType.incorrect_credentials_ip.value}:{self.ip}"
        value = await self.redis.get(key)
        counter = int(value) if value else 0
        counter += 1
        await self.redis.set(key, counter, ex=Config.ip_buffer_lifetime)
        if counter >= Config.ip_buffer:
            raise TooManyAttemptsFromIPException(self.ip)

    async def check_login_lock(
        self,
        tg_id: int
    ) -> None:
        key = f"{RedisType.invalidated_access_token.value}:{tg_id}"
        ttl = await self.redis.ttl(key)
        if ttl > 0:
            raise LoginLockedException(ttl)

    async def check_tg_code_gap(
        self,
        tg_id: int
    ) -> None:
        key = f"{RedisType.tg_code.value}:{tg_id}"
        ttl = await self.redis.ttl(key)
        if ttl > 0:
            gap = Config.tg_code_gap - Config.tg_code_lifetime + ttl
            if gap > 0:
                raise TooSoonToSendCodeException(gap)
