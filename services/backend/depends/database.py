
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    ActivePeriodRepository,
    MessageForTicketRepository,
    ServerInboundRepository,
    ServerRepository,
    TariffRepository,
    TelegramMessageRepository,
    TicketRepository,
    TransactionRepository,
    UserRepository,
    session_manager
)


async def get_session(
    session: AsyncSession = Depends(session_manager.session)
) -> AsyncSession:
    return session


async def get_user_repo(
    session: AsyncSession = Depends(get_session)
) -> UserRepository:
    return UserRepository(session)


async def get_server_repo(
    session: AsyncSession = Depends(get_session)
) -> ServerRepository:
    return ServerRepository(session)


async def get_server_inbound_repo(
    session: AsyncSession = Depends(get_session)
) -> ServerInboundRepository:
    return ServerInboundRepository(session)


async def get_tariff_repo(
    session: AsyncSession = Depends(get_session)
) -> TariffRepository:
    return TariffRepository(session)


async def get_transaction_repo(
    session: AsyncSession = Depends(get_session)
) -> TransactionRepository:
    return TransactionRepository(session)


async def get_ticket_repo(
    session: AsyncSession = Depends(get_session)
) -> TicketRepository:
    return TicketRepository(session)


async def get_message_repo(
    session: AsyncSession = Depends(get_session)
) -> MessageForTicketRepository:
    return MessageForTicketRepository(session)


async def get_tg_message_repo(
    session: AsyncSession = Depends(get_session)
) -> TelegramMessageRepository:
    return TelegramMessageRepository(session)


async def get_active_period_repo(
    session: AsyncSession = Depends(get_session)
) -> ActivePeriodRepository:
    return ActivePeriodRepository(session)
