
import uuid
from datetime import datetime


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.telegram_message import TelegramMessage
from database.models.user import User


class TelegramMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, text: str, date: datetime, sender: User, recipient: User) -> TelegramMessage | None:
        telegram_message = TelegramMessage(text=text, date=date, sender_id=sender.id, recipient_id=recipient.id)
        self.session.add(telegram_message)
        await self.session.flush()
        return await self.get_by_id(telegram_message.id)
    
    async def get_by_id(self, id: uuid.UUID) -> TelegramMessage | None:
        stmt = select(TelegramMessage).where(TelegramMessage.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_by_sender(self, sender: User) -> list[TelegramMessage]:
        stmt = select(TelegramMessage).where(TelegramMessage.sender_id == sender.id)
        return list((await self.session.scalars(stmt)).all())
    
    async def get_by_recipient(self, recipient: User) -> list[TelegramMessage]:
        stmt = select(TelegramMessage).where(TelegramMessage.sender_id == recipient.id)
        return list((await self.session.scalars(stmt)).all())