

from uuid import UUID

from httpx import AsyncClient

from .utils import check_response


async def get_all(base_url: str,
                  httpx_client: AsyncClient
                  ) -> None:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)


async def count(base_url: str,
                httpx_client: AsyncClient
                ) -> None:
    response = await httpx_client.get(base_url + "/count")
    check_response(base_url + "/count", "GET", response)


async def patch(base_url: str,
                user_id: UUID,
                httpx_client: AsyncClient
                ) -> None:
    response = await httpx_client.patch(f"{base_url}/{user_id}", json={
        "description": "new description"
    })
    check_response(f"{base_url}/{user_id}", "PATCH", response)


async def me(base_url: str,
             httpx_client: AsyncClient
             ) -> UUID:
    response = await httpx_client.get(base_url + "/me")
    check_response(base_url + "/me", "GET", response)
    return response.json()["id"]


async def user_test(base_url: str,
                    httpx_client: AsyncClient
                    ) -> UUID:
    await get_all(base_url, httpx_client)
    await count(base_url, httpx_client)
    id = await me(base_url, httpx_client)
    await patch(base_url, id, httpx_client)
    return id
