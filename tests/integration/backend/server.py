
from datetime import UTC, datetime, timedelta
from uuid import UUID

from httpx import AsyncClient

from .utils import check_response


async def create(base_url: str,
                 httpx_client: AsyncClient
                 ) -> None:
    date = datetime.now(UTC).replace(tzinfo=None)
    date_plus = date + timedelta(days=30)
    date = date.replace(tzinfo=None)
    date_plus = date_plus.replace(tzinfo=None)
    server = {
        "ip": "127.0.0.1",
        "description": "custom_description",
        "panel_port": 0,
        "port_generator_port": 0,
        "web_path": "custom_path",
        "country_code": "us",
        "is_available": True,
        "display_name": "custom_name",
        "login": "login",
        "password": "password",
        "starting_date": date.isoformat(),
        "closing_date": date_plus.isoformat(),
        "vless_reality_id": 0,
        "vless_reality_port": 0,
        "vless_reality_domain_short_id": "custom_domain_short_id",
        "vless_reality_public_key": "custom_public_key",
        "vless_reality_private_key": "custom_private_key"
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
        "ip": "0.0.0.0"
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
