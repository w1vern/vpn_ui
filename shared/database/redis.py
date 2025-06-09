
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
        host=settings.redis.ip,
        port=settings.redis.port,
        db=0,
        decode_responses=True)
