from sqlalchemy.orm import Session
from sqlalchemy import UUID, select
from app.database.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: UUID) -> User | None:
        stmt = select(User).where(User.id == id).limit(1)
        return self.session.scalar(stmt)
    
    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id).limit(1)
        return self.session.scalar(stmt)
    
    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.session.scalars(stmt).all())
    
    def create(self, telegram_id: int) -> None:
        user = User(telegram_id = telegram_id)
        self.session.add(user)
        self.session.commit()
        
    def set_telegram_username(self, user: User) -> None:
        user.telegram_username = "Steel Abobus"
        self.session.commit()
