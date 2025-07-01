
from redis.asyncio import Redis

from shared.config import env_config


def get_redis_client(db: int) -> Redis:
    return Redis(
        host=env_config.redis.ip,
        port=env_config.redis.port,
        db=db,
        decode_responses=True)