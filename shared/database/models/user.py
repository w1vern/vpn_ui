
from uuid import UUID

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel
from .tariff import Tariff


class UserSettings(Base):
    __tablename__ = "user_settings"
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    get_traffic_notifications: Mapped[bool] = mapped_column(default=True)
    auto_pay: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    language_code: Mapped[str] = mapped_column(default="en")


class UserRights(Base):
    __tablename__ = "user_rights"
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    is_admin_rights_editor: Mapped[bool] = mapped_column(default=False)
    is_member_rights_editor: Mapped[bool] = mapped_column(default=False)
    is_users_editor: Mapped[bool] = mapped_column(default=False)
    is_servers_editor: Mapped[bool] = mapped_column(default=False)
    is_control_panel_user: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_transactions_editor: Mapped[bool] = mapped_column(default=False)
    is_tariffs_editor: Mapped[bool] = mapped_column(default=False)


class User(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True
    )
    tariff_id: Mapped[UUID] = mapped_column(ForeignKey("tariffs.id"))
    telegram_username: Mapped[str] = mapped_column()
    internal_id: Mapped[str] = mapped_column(unique=True)
    panel_id: Mapped[UUID] = mapped_column()
    description: Mapped[str] = mapped_column()
    balance: Mapped[int] = mapped_column()
    secret: Mapped[str] = mapped_column()

    tariff: Mapped[Tariff] = relationship(
        lazy="selectin", foreign_keys=[tariff_id])

    rights: Mapped[UserRights] = relationship(
        "UserRights",
        uselist=False,
        backref="user",
        lazy="selectin"
    )

    settings: Mapped[UserSettings] = relationship(
        "UserSettings",
        uselist=False,
        backref="user",
        lazy="selectin"
    )
