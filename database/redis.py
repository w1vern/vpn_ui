from enum import Enum

import redis
import redis.client


class RedisType(str, Enum):
    tg_code = "tg_code"


def get_redis_client() -> redis.client.Redis:
    return redis.Redis(host='localhost', port=6379, db=0)