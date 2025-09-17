
import httpx

from shared.infrastructure import get_redis_client, RedisDatabase
from .auth import auth_test
from .server import servers_test
from shared.config import env_config
from shared.infrastructure.logger import setup_logger

logger = setup_logger(__name__)


async def run_backend_test() -> None:
    redis = get_redis_client(db=RedisDatabase.backend.value)
    url = f"http://{env_config.backend.ip}:{env_config.backend.port}/api/"
    async with httpx.AsyncClient() as httpx_client:
        await auth_test(url + "auth", env_config.bot.superuser, redis, httpx_client)
        logger.debug("auth test complete")
        await servers_test(url + "servers", httpx_client)
        logger.debug("servers test complete")
    logger.debug("integration backend tests complete")
