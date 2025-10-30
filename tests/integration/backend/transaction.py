
from datetime import UTC, datetime
from uuid import UUID

from httpx import AsyncClient

from shared.infrastructure import setup_logger

from .utils import check_response

logger = setup_logger(__name__)


async def get(base_url: str,
              httpx_client: AsyncClient
              ) -> None:
    response = await httpx_client.get(base_url)
    check_response(base_url, "GET", response)


async def count(base_url: str,
                httpx_client: AsyncClient
                ) -> None:
    response = await httpx_client.get(base_url + "/count")
    check_response(base_url + "/count", "GET", response)


async def create(base_url: str,
                 user_id: UUID,
                 httpx_client: AsyncClient
                 ) -> None:
    transaction = {
        "user_id": str(user_id),
        "amount": 100.5,
        "description": "new transaction",
        "transaction_type": "withdrawal",
        "date": datetime.now(UTC).replace(tzinfo=None).isoformat()
    }
    response = await httpx_client.post(base_url, json=transaction)
    check_response(base_url, "POST", response)


async def transaction_test(user_id: UUID,
                           base_url: str,
                           httpx_client: AsyncClient
                           ) -> None:
    await get(base_url, httpx_client)
    await count(base_url, httpx_client)
    await create(base_url, user_id, httpx_client)
