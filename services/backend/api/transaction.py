

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (TransactionRepository, TransactionType, User,
                             UserRepository, session_manager)

from ..get_auth import get_user
from ..schemas import Transaction, UserSchema

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post(
    path="",
    summary="Create a new transaction"
)
async def create_transaction(transaction_to_create: Transaction,
                             user: UserSchema = Depends(get_user),
                             session: AsyncSession = Depends(
                                 session_manager.session)
                             ):
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
                               ) -> list[Transaction]:
    if user.rights.is_control_panel_user is False:
        raise HTTPException(status_code=403, detail="no rights")
    tr = TransactionRepository(session)
    transactions = await tr.get_all()
    tr_to_send = []
    for transaction in transactions:
        tr_to_send.append(Transaction(user_id=str(transaction.user_id), amount=transaction.amount,
                                      date=transaction.date.isoformat(), type=TransactionType(transaction.transaction_type).name))
    return tr_to_send
