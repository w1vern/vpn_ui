
from enum import Enum

from redis.asyncio import Redis

from shared.infrastructure import get_redis_client as gr


class RedisType(str, Enum):
    main_message = "main_message"
    state = "state"


def get_redis_client() -> Redis:
    return gr(db=1)