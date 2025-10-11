
from httpx import AsyncClient

from .utils import check_response


async def create(base_url: str, httpx_client: AsyncClient) -> None:
    payload = {
        "data": {
            "en": "en text",
            "ru": "ru text"
        }}
    response = await httpx_client.post(base_url, json=payload)
    check_response(base_url, "POST", response)


async def notification_test(base_url: str, httpx_client: AsyncClient) -> None:
    await create(base_url, httpx_client)
