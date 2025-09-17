
import httpx

from shared.config import env_config
from shared.infrastructure import (
    RedisDatabase,
    get_redis_client,
    setup_logger
)

from .auth import auth_test
from .server import server_test
from .user import user_test
from .tariff import tariff_test
from .transaction import transaction_test
from .notification import notification_test
from .ticket import ticket_test

logger = setup_logger(__name__)


async def run_backend_test() -> None:
    redis = get_redis_client(db=RedisDatabase.backend.value)
    url = f"http://{env_config.backend.ip}:{env_config.backend.port}/api/"
    async with httpx.AsyncClient() as httpx_client:
        await auth_test(url + "auth", env_config.bot.superuser, redis, httpx_client)
        logger.debug("auth test complete")
        await server_test(url + "servers", httpx_client)
        logger.debug("server test complete")
        user_id = await user_test(url + "users", httpx_client)
        logger.debug("user test complete")
        await tariff_test(url + "tariffs", httpx_client)
        logger.debug("tariff test complete")
        await transaction_test(user_id, url + "transactions", httpx_client)
        logger.debug("transaction test complete")
        await notification_test(url + "notifications", httpx_client)
        logger.debug("notification test complete")
        await ticket_test(url + "tickets", httpx_client)
        logger.debug("ticket test complete")
    logger.debug("integration backend tests complete")
