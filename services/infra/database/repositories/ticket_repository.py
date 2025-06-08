
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Ticket, User

from .base_repository import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Ticket)


    async def create(self,
                     title: str,
                     holder: User,
                     opening_date: datetime | None = None,
                     closing_date: datetime | None = None,
                     is_open: bool = True
                     ) -> Ticket | None:
        if opening_date is None:
            opening_date = datetime.now(UTC).replace(tzinfo=None)
        if closing_date is None:
            closing_date = datetime.now(UTC).replace(tzinfo=None)
        return await self.universal_create(
            title=title,
            holder_id=holder.id,
            opening_date=opening_date,
            closing_date=closing_date,
            is_open=is_open)

    async def get_all_for_user(self,
                               holder: User
                               ) -> list[Ticket]:
        stmt = select(Ticket).where(
            Ticket.holder_id == holder.id)
        return list((await self.session.scalars(stmt)).all())

    async def get_all_opened(self
                             ) -> list[Ticket]:
        stmt = select(Ticket).where(Ticket.is_open == True)
        return list((await self.session.scalars(stmt)).all())

    async def close(self,
                    ticket: Ticket
                    ) -> None:
        ticket.closing_date = datetime.now(UTC)
        ticket.is_open = False
        await self.session.flush()
