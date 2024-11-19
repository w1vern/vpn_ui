from datetime import UTC, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, title: str, holder: User, opening_date: datetime = datetime.now(UTC).replace(tzinfo=None), closing_date: datetime = datetime.now(UTC).replace(tzinfo=None), is_open: bool = True):
        ticket = Ticket(title=title, holder_id=holder.id,
                        opening_date=opening_date, closing_date=closing_date, is_open=is_open)
        self.session.add(ticket)
        await self.session.flush()

    async def get_by_id(self, id: UUID) -> Optional[Ticket]:
        stmt = select(Ticket).where(Ticket.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_all_for_user(self, holder: User) -> list[Ticket]:
        stmt = select(Ticket).where(Ticket.holder_id == holder.id)
        return list((await self.session.scalars(stmt)).all())
    
    async def get_all_opened(self) -> list[Ticket]:
        stmt = select(Ticket).where(Ticket.is_open == True)
        return list((await self.session.scalars(stmt)).all())
    
    async def get_all(self) -> list[Ticket]:
        stmt = select(Ticket)
        return list((await self.session.scalars(stmt)).all())
    
    async def close(self, ticket: Ticket) -> None:
        ticket.closing_date = datetime.now(UTC)
        ticket.is_open = False
        await self.session.flush()
