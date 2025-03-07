from enum import Enum

import redis
import redis.client

from config import settings



class RedisType(str, Enum):
    tg_code = "tg_code"


def get_redis_client() -> redis.client.Redis:
    return redis.Redis(host=settings.redis_ip, port=settings.redis_port, db=0)
