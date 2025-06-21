
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    TransactionRepository,
    UserRepository
)

from ..schemas import (
    UserSchema,
    TransactionSchema
)
from .depends import (
    get_session,
    get_transaction_repo,
    get_user,
    get_db_user
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
                ur: UserRepository = Depends(get_db_user),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'TransactionService':
        return cls(session, tr, ur, user_schema)

    async def create(self,
                     transaction_to_create: TransactionSchema
                     ) -> None:
        
