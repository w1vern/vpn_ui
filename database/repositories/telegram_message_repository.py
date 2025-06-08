
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TelegramMessage, User

from .base_repository import BaseRepository


class TelegramMessageRepository(BaseRepository[TelegramMessage]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TelegramMessage)

    async def create(self,
                     text: str,
                     date: datetime,
                     sender: User,
                     recipient: User
                     ) -> TelegramMessage:
        return await self.universal_create(
            text=text,
            date=date,
            sender_id=sender.id,
            recipient_id=recipient.id)

    async def get_by_sender(self,
                            sender: User
                            ) -> list[TelegramMessage]:
        stmt = select(TelegramMessage).where(
            TelegramMessage.sender_id == sender.id)
        return list((await self.session.scalars(stmt)).all())

    async def get_by_recipient(self,
                               recipient: User
                               ) -> list[TelegramMessage]:
        stmt = select(TelegramMessage).where(
            TelegramMessage.sender_id == recipient.id)
        return list((await self.session.scalars(stmt)).all())
