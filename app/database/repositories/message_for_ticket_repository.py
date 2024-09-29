from sqlalchemy.orm import Session
from sqlalchemy import UUID, select
from app.database.models.message_for_ticket import MessageForTicket
from app.database.enums.message_ticket_type import MessageTicketType

class MessageForTicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_message_by_ticket(self, ticket_id: UUID) -> list[MessageForTicket]:
        stmt = select(MessageForTicket).where(MessageForTicket.ticket_id == ticket_id)
        return list(self.session.scalars(stmt).all())
    
    def create(self, text: str, ticket_id: UUID, type: MessageTicketType) -> None:
        self.session.add(MessageForTicket(text=text, ticket_id=ticket_id, type=type))
        self.session.flush()