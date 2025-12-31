
import random
from datetime import UTC, datetime, timedelta
from uuid import UUID

from httpx import AsyncClient

from .utils import check_response


async def create(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    date = datetime.now(UTC).replace(tzinfo=None)
    date_plus = date + timedelta(days=30)
    date = date.replace(tzinfo=None)
    date_plus = date_plus.replace(tzinfo=None)
    server = {
        "ip": f"{random.random()}",
        "secured": False,
        "description": "custom_description",
        "panel_port": 0,
        "panel_web_path": "custom_path",
        "country_code": "us",
        "display_name": "custom_name",
        "panel_login": "login",
        "panel_password": "password",
        "starting_date": date.isoformat(),
        "closing_date": date_plus.isoformat()
    }
    response = await httpx_client.post(base_url, json=server)
    check_response(base_url, "POST", response)


async def get_all(
    base_url: str,
    httpx_client: AsyncClient
) -> UUID:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)
    return response.json()[0]["id"]


async def count(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(base_url + "/count")
    check_response(base_url + "/count", "GET", response)


async def patch(
    server_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.patch(f"{base_url}/{server_id}", json={
        "ip": f"{random.random()}"
    })
    check_response(f"{base_url}/{server_id}", "PATCH", response)


async def get(
    server_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(f"{base_url}/{server_id}")
    check_response(base_url, "GET", response)


async def server_test(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    await create(base_url, httpx_client)
    await count(base_url, httpx_client)
    id = await get_all(base_url, httpx_client)
    await get(id, base_url, httpx_client)
    await patch(id, base_url, httpx_client)
