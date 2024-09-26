from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import UUID, ForeignKey
from app.database import Base

from uuid import uuid4

from datetime import datetime
from app.enums import TransactionType, Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    telegram_username: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[float] = mapped_column(default=0)
    role: Mapped[Role] = mapped_column()

    # ------------
    active: Mapped[bool] = mapped_column()
    auto_pay: Mapped[bool] = mapped_column()
    # ------------???


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    holder_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    holder: Mapped[User] = relationship(lazy="selectin")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column()
    ticket_id: Mapped[UUID] = mapped_column(ForeignKey("tickets.id"))
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    ticket: Mapped[Ticket] = relationship(lazy="selectin")
    sender: Mapped[User] = relationship(lazy="selectin")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    amount: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    type: Mapped[TransactionType] = mapped_column()


class ActivePeriod(Base):
    __tablename__ = "active_periods"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"))
    start_time: Mapped[datetime] = mapped_column()
    ending_time: Mapped[datetime] = mapped_column()

    user: Mapped[User] = relationship(lazy="selectin")
    transaction: Mapped[Transaction] = relationship(lazy="selectin")
