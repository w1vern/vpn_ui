
from enum import Enum

from redis.asyncio import Redis

from config import settings


class RedisType(str, Enum):
    tg_code = "tg_code",
    incorrect_credentials = "incorrect_credentials",
    invalidated_access_token = "invalidated_access_token"
    incorrect_credentials_ip = "incorrect_credentials_ip"


def get_redis_client() -> Redis:
    return Redis(
        host=settings.redis_ip,
        port=settings.redis_port,
        db=0)
