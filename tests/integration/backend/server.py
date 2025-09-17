
from typing import Any
from uuid import UUID
from httpx import AsyncClient

from datetime import datetime, UTC, timedelta
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
        "closing_date": date_plus.isoformat()
    }
    response = await httpx_client.post(base_url, json=server)
    check_response(base_url, "POST", response)


async def get(base_url: str,
              httpx_client: AsyncClient
              ) -> UUID:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)
    return response.json()[0]["id"]


async def patch(base_url: str,
                server_id: UUID,
                httpx_client: AsyncClient
                ) -> None:
    response = await httpx_client.patch(f"{base_url}/{server_id}", json={
        "ip": "0.0.0.0"
    })
    check_response(f"{base_url}/{server_id}", "PATCH", response)


async def servers_test(base_url: str,
                       httpx_client: AsyncClient
                       ) -> None:
    await create(base_url, httpx_client)
    id = await get(base_url, httpx_client)
    await patch(base_url, id, httpx_client)
