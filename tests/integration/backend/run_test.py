
import httpx

from shared.infrastructure import (
    env_config,
    get_redis_client,
    setup_logger
)

from .auth import auth_test
from .notification import notification_test
from .server import server_test
from .tariff import tariff_test
from .ticket import ticket_test
from .transaction import transaction_test
from .user import user_test

logger = setup_logger(__name__)


async def run_backend_test() -> None:
    redis = get_redis_client(db=env_config.redis.backend)
    url = f"http://localhost:8000/api/"
    async with httpx.AsyncClient() as httpx_client:
        await auth_test(url + "auth", env_config.bot.superuser, redis, httpx_client)
        logger.info("auth test complete")
        await server_test(url + "servers", httpx_client)
        logger.info("server test complete")
        user_id = await user_test(url + "users", httpx_client)
        logger.info("user test complete")
        await tariff_test(url + "tariffs", httpx_client)
        logger.info("tariff test complete")
        await transaction_test(user_id, url + "transactions", httpx_client)
        logger.info("transaction test complete")
        await notification_test(url + "notifications", httpx_client)
        logger.info("notification test complete")
        await ticket_test(url + "tickets", httpx_client)
        logger.info("ticket test complete")
    logger.info("integration backend tests complete")
