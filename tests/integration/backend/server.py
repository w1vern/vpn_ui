
import random
from datetime import UTC, datetime, timedelta
from uuid import UUID

from httpx import AsyncClient

from .utils import check_response


async def create(
    base_url: str,
    httpx_client: AsyncClient
) -> UUID:
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
    return UUID(response.json()["id"])


async def get_all(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)


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


async def get_all_inbound_protocols(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(base_url + "/inbounds/protocols")
    check_response(base_url + "/inbound_protocols", "GET", response)


async def get_all_inbounds(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(base_url + "/inbounds")
    check_response(base_url + "/inbounds", "GET", response)


async def inbounds_count(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(base_url + "/inbounds/count")
    check_response(base_url + "/inbounds/count", "GET", response)


async def create_inbound(
    server_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> UUID:
    inbound = {
       "inbound_id": 1,
       "template": "{user_id}#{comment}",
        "protocol": "vless",
        "name": "inbound_name",
        "description": "",
        "is_available": True
    }
    response = await httpx_client.post(base_url + f"/inbounds/{server_id}", json=inbound)
    check_response(base_url + "/inbounds", "POST", response)
    return UUID(response.json()["id"])


async def delete_inbound(
    inbound_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.delete(base_url + f"/inbounds/{inbound_id}")
    check_response(base_url + "/inbounds", "DELETE", response)

async def get_inbound(
    inbound_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(base_url + f"/inbounds/{inbound_id}")
    check_response(base_url + "/inbounds", "GET", response)

async def patch_inbound(
    inbound_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.patch(base_url + f"/inbounds/{inbound_id}", json={
        "ip": f"{random.random()}"
    })
    check_response(base_url + "/inbounds", "PATCH", response)


async def server_test(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    id = await create(base_url, httpx_client)
    await count(base_url, httpx_client)
    await get_all(base_url, httpx_client)
    await get(id, base_url, httpx_client)
    await patch(id, base_url, httpx_client)

    inbound_id = await create_inbound(id, base_url, httpx_client)
    await get_all_inbound_protocols(base_url, httpx_client)
    await get_all_inbounds(base_url, httpx_client)
    await inbounds_count(base_url, httpx_client)
    await get_inbound(inbound_id, base_url, httpx_client)
    await patch_inbound(inbound_id, base_url, httpx_client)
    await delete_inbound(inbound_id, base_url, httpx_client)
