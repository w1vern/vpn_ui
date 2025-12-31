
from uuid import UUID

from httpx import AsyncClient

from shared.database import (
    TicketRepository,
    UserRepository,
    session_manager
)

from .utils import check_response


async def get_all(
    base_url: str,
    httpx_client: AsyncClient
) -> UUID:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)
    return response.json()[0]["id"]


async def get(
    ticket_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.get(f"{base_url}/{ticket_id}")
    check_response(base_url, "GET", response)


async def close(
    ticket_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    response = await httpx_client.patch(f"{base_url}/{ticket_id}/close")
    check_response(base_url, "PATCH", response)


async def new_message(
    ticket_id: UUID,
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    message = {
        "message": "new answer"
    }
    response = await httpx_client.post(f"{base_url}/{ticket_id}/messages", json=message)
    check_response(base_url, "POST", response)


async def ticket_test(
    base_url: str,
    httpx_client: AsyncClient
) -> None:
    async with session_manager.context_session() as session:
        ur = UserRepository(session)
        user = (await ur.get_all())[0]
        tr = TicketRepository(session)
        ticket = await tr.create(title="test title", holder=user)
    if ticket is None:
        raise Exception("Failed to create ticket")
    id = ticket.id
    await new_message(id, base_url, httpx_client)
    id = await get_all(base_url, httpx_client)
    await get(id, base_url, httpx_client)
    await close(id, base_url, httpx_client)
