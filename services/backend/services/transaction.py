
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from shared.database import (
    TransactionRepository,
)

from ..schemas import (
    UserSchema,
)
from .depends import (
    get_session,
    get_transaction_repo,
    get_user,
)


class TransactionService:
    def __init__(self,
                 session: AsyncSession,
                 tr: TransactionRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.tr = tr
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                      session: AsyncSession = Depends(get_session),
                      tr: TransactionRepository = Depends(
                          get_transaction_repo),
                      user_schema: UserSchema = Depends(get_user)
                      ) -> 'TransactionService':
        return cls(session, tr, user_schema)
