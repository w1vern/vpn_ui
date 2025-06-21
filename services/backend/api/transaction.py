

import uuid
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from ..response import SuccessResponse

from ..services import TransactionService
from shared.database import (
    TransactionRepository,
    TransactionType,
    UserRepository,
    session_manager,
)

from ..schemas import (
    TransactionSchema,
    UserSchema,
)

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post(
    path="",
    summary="Create a new transaction"
)
async def create_transaction(transaction_to_create: TransactionSchema,
                             transaction_service: TransactionService = Depends(
                                 TransactionService.depends)
                             ) -> SuccessResponse:
    if user.rights.is_control_panel_user is False:
        raise HTTPException(status_code=403, detail="no rights")
    if user.rights.is_transaction_editor is False:
        raise HTTPException(status_code=403, detail="no rights")
    tr = TransactionRepository(session)
    ur = UserRepository(session)
    tr_user = await ur.get_by_id(uuid.UUID(transaction_to_create.user_id))
    if tr_user is None:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    date = None
    if transaction_to_create.date is not None:
        date = datetime.fromisoformat(transaction_to_create.date)
    type = getattr(TransactionType, transaction_to_create.type)
    if type is None:
        raise HTTPException(
            status_code=404, detail="Transaction type doesn't exist")
    await tr.create(tr_user, transaction_to_create.amount, date, type.value)
    return {"message": "OK"}


@router.get(
    path="/all",
    summary="Get all transactions"
)
async def get_all_transactions(user: UserSchema = Depends(get_user),
                               session: AsyncSession = Depends(
                                   session_manager.session)
                               ) -> list[TransactionSchema]:
    if user.rights.is_control_panel_user is False:
        raise HTTPException(status_code=403, detail="no rights")
    tr = TransactionRepository(session)
    transactions = await tr.get_all()
    tr_to_send: list[TransactionSchema] = []
    for transaction in transactions:
        tr_to_send.append(TransactionSchema(user_id=str(transaction.user_id), amount=transaction.amount,
                                      date=transaction.date.isoformat(), type=TransactionType(transaction.transaction_type).name))
    return tr_to_send
