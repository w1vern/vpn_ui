from sqlalchemy.orm import Session
from sqlalchemy import UUID, select
from app.database.models.message_for_ticket import Message

class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_message_by_sender(self, sender_id: UUID) -> list[Message]:
        stmt = select(Message).where(Message.sender_id == sender_id)
        return list(self.session.scalars(stmt).all())
    
    def create(self, text: str, ticket_id: UUID, sender_id: UUID)