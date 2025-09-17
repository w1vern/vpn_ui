
import random
from uuid import UUID
from .utils import check_response

from httpx import AsyncClient


async def get_all(base_url: str,
                  httpx_client: AsyncClient
                  ) -> UUID:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)
    return response.json()[1]["id"]


async def create(base_url: str,
                 httpx_client: AsyncClient
                 ) -> None:
    tariff = {
        "name": f"test tariff {random.random}",
        "duration": 3600,
        "description": "test description",
        "price": 100,
        "price_of_traffic_reset": 50,
        "traffic": 1000,
        "is_special": False
    }
    response = await httpx_client.post(base_url, json=tariff)
    check_response(base_url, "POST", response)


async def get(tariff_id: UUID,
              base_url: str,
              httpx_client: AsyncClient
              ) -> None:
    response = await httpx_client.get(f"{base_url}/{tariff_id}")
    check_response(base_url, "GET", response)


async def delete(tariff_id: UUID,
                 base_url: str,
                 httpx_client: AsyncClient
                 ) -> None:
    response = await httpx_client.delete(f"{base_url}/{tariff_id}")
    check_response(base_url, "DELETE", response)


async def patch(tariff_id: UUID,
                base_url: str,
                httpx_client: AsyncClient
                ) -> None:
    response = await httpx_client.patch(f"{base_url}/{tariff_id}", json={
        "description": "new description"
    })
    check_response(f"{base_url}/{tariff_id}", "PATCH", response)


async def tariff_test(base_url: str,
                      httpx_client: AsyncClient
                      ) -> None:
    await create(base_url, httpx_client)
    id = await get_all(base_url, httpx_client)
    await patch(id, base_url, httpx_client)
    await get(id, base_url, httpx_client)
    await delete(id, base_url, httpx_client)
