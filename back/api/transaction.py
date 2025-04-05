

import uuid
from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi_controllers import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from back.get_auth import get_user
from back.schemas.transaction import Transaction
from back.schemas.user import UserSchema
from database.database import get_db_session
from database.enums.transaction_type import TransactionType
from database.models.user import User
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.user_repository import UserRepository


class TransactionController(Controller):
    prefix = "/transaction"
    tags = ["transaction"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    @post("/create")
    async def create_transaction(self, transaction_to_create: Transaction, user: UserSchema = Depends(get_user)):
        if user.rights.is_control_panel_user is False:
            raise HTTPException(status_code=403, detail="no rights")
        if user.rights.is_transaction_editor is False:
            raise HTTPException(status_code=403, detail="no rights")
        tr = TransactionRepository(self.session)
        ur = UserRepository(self.session)
        tr_user = await ur.get_by_id(uuid.UUID(transaction_to_create.user_id))
        if tr_user is None:
            raise HTTPException(status_code=404, detail="User doesn't exist")
        date = None
        if transaction_to_create.date is not None:
            date = datetime.fromisoformat(transaction_to_create.date)
        type = getattr(TransactionType, transaction_to_create.type)
        if type is None:
            raise HTTPException(status_code=404, detail="Transaction type doesn't exist")
        await tr.create(tr_user, transaction_to_create.amount, date, type.value)
        return {"message": "OK"}
    
    @get("/get_all")
    async def get_all_transactions(self, user: UserSchema = Depends(get_user)) -> list[Transaction]:
        if user.rights.is_control_panel_user is False:
            raise HTTPException(status_code=403, detail="no rights")
        tr = TransactionRepository(self.session)
        transactions = await tr.get_all()
        tr_to_send = []
        for transaction in transactions:
            tr_to_send.append(Transaction(user_id=str(transaction.user_id), amount=transaction.amount, date=transaction.date.isoformat(), type=TransactionType(transaction.type).name))
        return tr_to_send


