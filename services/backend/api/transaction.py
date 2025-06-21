
from fastapi import (
    APIRouter,
    Depends,
)

from ..response import SuccessResponse
from ..schemas import TransactionSchema
from ..services import TransactionService

router = APIRouter(prefix="/transaction", tags=["transaction"])


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
    path="/all",
    summary="Get all transactions"
)
async def all(transaction_service: TransactionService = Depends(TransactionService.depends)
              ) -> list[TransactionSchema]:
    return await transaction_service.all()
