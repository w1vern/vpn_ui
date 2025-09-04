
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    TransactionRepository,
    TransactionType,
    UserRepository
)

from ..exceptions import (
    TransactionTypeNotFoundException,
    UserNotFoundException,
    UserNotTransactionEditorException
)
from ..schemas import TransactionSchema, UserSchema
from .depends import (
    get_session,
    get_transaction_repo,
    get_user,
    get_user_repo
)


class TransactionService:
    def __init__(self,
                 session: AsyncSession,
                 tr: TransactionRepository,
                 ur: UserRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.tr = tr
        self.ur = ur
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                tr: TransactionRepository = Depends(
                    get_transaction_repo),
                ur: UserRepository = Depends(get_user_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'TransactionService':
        return cls(session, tr, ur, user_schema)

    async def create(self,
                     transaction_to_create: TransactionSchema
                     ) -> None:
        if self.user_schema.rights.is_transaction_editor is False:
            raise UserNotTransactionEditorException
        tr_user = await self.ur.get_by_id(transaction_to_create.user_id)
        if tr_user is None:
            raise UserNotFoundException()
        type: TransactionType = getattr(
            TransactionType, transaction_to_create.transaction_type)
        if type is None:
            raise TransactionTypeNotFoundException()
        if not transaction_to_create.date is None:
            transaction_to_create.date.replace(tzinfo=None)
        await self.tr.create(tr_user,
                             transaction_to_create.amount,
                             transaction_to_create.description,
                             transaction_to_create.date,
                             type.value)
        await self.ur.update_balance(tr_user, transaction_to_create.amount)

    async def all(self,
                  user_id: UUID | None,
                  limit: int | None,
                  offset: int | None
                  ) -> list[TransactionSchema]:
        return [TransactionSchema.from_db(t)
                for t in await self.tr.get_all(limit, offset, user_id=user_id)]

    async def count(self,
                    user_id: UUID | None
                    ) -> int:
        if user_id is None:
            return await self.tr.count()
        return await self.tr.count(user_id=user_id)
