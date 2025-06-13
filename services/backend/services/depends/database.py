
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from shared.database import (
    ActivePeriodRepository,
    MessageForTicketRepository,
    PanelServerRepository,
    ServerRepository,
    ServerUserInboundRepository,
    TariffRepository,
    TelegramMessageRepository,
    TgBotTokenRepository,
    TicketRepository,
    TransactionRepository,
    UserRepository,
    session_manager,
)


async def get_session(session: AsyncSession = Depends(session_manager.session)
                      ) -> AsyncSession:
    return session


async def get_user_repo(session: AsyncSession = Depends(session_manager.session)
                        ) -> UserRepository:
    return UserRepository(session)


async def get_server_repo(session: AsyncSession = Depends(session_manager.session)
                          ) -> ServerRepository:
    return ServerRepository(session)


async def get_panel_server_repo(session: AsyncSession = Depends(session_manager.session)
                                ) -> PanelServerRepository:
    return PanelServerRepository(session)


async def get_tariff_repo(session: AsyncSession = Depends(session_manager.session)
                          ) -> TariffRepository:
    return TariffRepository(session)


async def get_transaction_repo(session: AsyncSession = Depends(session_manager.session)
                               ) -> TransactionRepository:
    return TransactionRepository(session)


async def get_ticket_repo(session: AsyncSession = Depends(session_manager.session)
                          ) -> TicketRepository:
    return TicketRepository(session)


async def get_message_repo(session: AsyncSession = Depends(session_manager.session)
                           ) -> MessageForTicketRepository:
    return MessageForTicketRepository(session)


async def get_tg_message_repo(session: AsyncSession = Depends(session_manager.session)
                              ) -> TelegramMessageRepository:
    return TelegramMessageRepository(session)


async def get_active_period_repo(session: AsyncSession = Depends(session_manager.session)
                                 ) -> ActivePeriodRepository:
    return ActivePeriodRepository(session)


async def get_tg_bot_token_repo(session: AsyncSession = Depends(session_manager.session)
                                ) -> TgBotTokenRepository:
    return TgBotTokenRepository(session)


async def get_server_user_inbound_repo(session: AsyncSession = Depends(session_manager.session)
                                       ) -> ServerUserInboundRepository:
    return ServerUserInboundRepository(session)
