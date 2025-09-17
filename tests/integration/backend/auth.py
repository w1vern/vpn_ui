
from httpx import AsyncClient
from redis.asyncio import Redis

from shared.infrastructure import setup_logger

from .utils import check_response

logger = setup_logger(__name__)


async def login(base_url: str,
                user_tg_id: int,
                redis: Redis,
                httpx_client: AsyncClient
                ) -> None:
    response = await httpx_client.post(base_url + "/tg_code", json={
        "tg_id": user_tg_id
    })
    code = await redis.get(f"tg_code:{user_tg_id}")

    check_response(base_url + "/tg_code", "POST", response)

    if code is None:
        raise Exception(f"Nothing in Redis")
    code = str(code)

    response = await httpx_client.post(base_url + "/login", json={
        "tg_id": user_tg_id,
        "tg_code": code
    })

    check_response(base_url + "/login", "POST", response)


async def logout(base_url: str,
                 httpx_client: AsyncClient
                 ) -> None:
    response = await httpx_client.post(base_url + "/logout")
    check_response(base_url + "/logout", "POST", response)


async def refresh(base_url: str,
                  httpx_client: AsyncClient
                  ) -> None:
    response = await httpx_client.post(base_url + "/refresh")
    check_response(base_url + "/refresh", "POST", response)


async def auth_test(base_url: str,
                    user_tg_id: int,
                    redis: Redis,
                    httpx_client: AsyncClient
                    ) -> None:
    await login(base_url, user_tg_id, redis, httpx_client)
    await logout(base_url, httpx_client)
    await login(base_url, user_tg_id, redis, httpx_client)
    await refresh(base_url, httpx_client)
