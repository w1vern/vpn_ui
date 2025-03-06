from enum import Enum
import os

from dotenv import load_dotenv
import redis
import redis.client


load_dotenv()


REDIS_IP = os.getenv("REDIS_IP")
REDIS_PORT = os.getenv("REDIS_PORT")

if REDIS_IP is None or REDIS_PORT is None:
    raise Exception("REDIS_IP or REDIS_PORT is not set")

REDIS_PORT = int(REDIS_PORT)


class RedisType(str, Enum):
    tg_code = "tg_code"


def get_redis_client() -> redis.client.Redis:
    return redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=0)  # type: ignore
