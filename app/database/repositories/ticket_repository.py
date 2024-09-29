from sqlalchemy.orm import Session
from sqlalchemy import UUID, select

from datetime import datetime, UTC
from typing import Optional


from app.database.models.ticket import Ticket

class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, holder_id: UUID, opening_date: datetime = datetime.now(UTC), closing_date: datetime = datetime.now(UTC), is_open: bool = True):
        ticket = Ticket(title=title, holder_id=holder_id,
                        opening_date=opening_date, closing_date=closing_date, is_open=is_open)
        self.session.add(ticket)
        self.session.flush()

    def get_by_id(self, id: UUID) -> Optional[Ticket]:
        stmt = select(Ticket).where(Ticket.id == id).limit(1)
        return self.session.scalar(stmt)
    
    def get_all_for_user(self, holder_id: UUID) -> list[Ticket]:
        stmt = select(Ticket).where(Ticket.holder_id == holder_id)
        return list(self.session.scalars(stmt).all())
    
    def get_all_opened(self) -> list[Ticket]:
        stmt = select(Ticket).where(Ticket.is_open == True)
        return list(self.session.scalars(stmt).all())
    
    def get_all(self) -> list[Ticket]:
        stmt = select(Ticket)
        return list(self.session.scalars(stmt).all())
    
    def close(self, id: UUID) -> None:
        ticket = self.get_by_id(id)
        ticket.closing_date = datetime.now(UTC)
        ticket.is_open = False
        self.session.flush()
