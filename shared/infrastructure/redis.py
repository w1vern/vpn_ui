
from enum import Enum

from redis.asyncio import Redis

from shared.config import env_config


class RedisType(str, Enum):
    tg_code = "tg_code",
    incorrect_credentials = "incorrect_credentials",
    invalidated_access_token = "invalidated_access_token"
    incorrect_credentials_ip = "incorrect_credentials_ip"

    bot_message = "bot_message"


def get_redis_client() -> Redis:
    return Redis(
        host=env_config.redis.ip,
        port=env_config.redis.port,
        db=0,
        decode_responses=True)
