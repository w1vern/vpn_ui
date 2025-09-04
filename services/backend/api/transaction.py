
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from ..response import SuccessResponse
from ..schemas import TransactionSchema
from ..services import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    path="",
    summary="Create a new transaction"
)
async def create(transaction_to_create: TransactionSchema,
                 transaction_service: TransactionService = Depends(
                     TransactionService.depends)
                 ) -> SuccessResponse:
    await transaction_service.create(transaction_to_create)
    return SuccessResponse()


@router.get(
    path="",
    summary="Get all transactions"
)
async def all(user_id: UUID | None = Query(None,
                                           description="User id"),
              limit: int | None = Query(None,
                                        ge=1,
                                        description="Number of items to return"),
              offset: int | None = Query(None,
                                         ge=0,
                                         description="From which index to start"),
              transaction_service: TransactionService = Depends(
        TransactionService.depends)) -> list[TransactionSchema]:
    return await transaction_service.all(user_id, limit, offset)

@router.get(
    path="/count",
    summary="Get transactions count"
)
async def count(user_id: UUID | None = Query(None,
                                            description="User id"),
                transaction_service: TransactionService = Depends(
        TransactionService.depends)) -> int:
    return await transaction_service.count(user_id)
