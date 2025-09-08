
from typing import Awaitable, Callable

from fast_depends import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared._3x_ui_ import Service as PanelService
from shared._3x_ui_ import server_session_manager
from shared.database import (
    PanelServerRepository,
    ServerRepository,
    ServerUserInbound,
    ServerUserInboundRepository,
    TariffRepository,
    TransactionRepository,
    UserRepository,
    session_manager
)
from shared.infrastructure import setup_logger
from shared.proxy_interface import (
    AccessConfig,
    AccessType,
    VpnConfig,
    VpnType
)

from .buttons import (
    StaticButtons,
    inbounds_keyboard,
    main_menu_keyboard,
    transactions_keyboard,
)
from .depends import (
    get_main_message,
    get_panel_server_repo,
    get_request_data,
    get_server_repo,
    get_server_user_inbound_repo,
    get_tariff_repo,
    get_transaction_repo,
    get_user_info,
    get_user_repo
)
from .exceptions import SendFeedbackToAdminException
from .i18n import I18nMessage, MessageKey
from .models import MainMessage, Notification, Output, UserInfo
from .redis import RedisType, get_redis_client

logger = setup_logger(__name__)


class Service():
    def __init__(self,
                 user_info: UserInfo,
                 main_message: MainMessage,
                 redis: Redis,
                 session: AsyncSession,
                 ur: UserRepository,
                 sr: ServerRepository,
                 suir: ServerUserInboundRepository,
                 tfr: TariffRepository,
                 psr: PanelServerRepository,
                 tr: TransactionRepository,
                 input: str
                 ) -> None:
        self.user_info = user_info
        self.main_message = main_message
        self.redis = redis
        self.session = session
        self.ur = ur
        self.sr = sr
        self.suir = suir
        self.tfr = tfr
        self.psr = psr
        self.tr = tr
        self.input = input

        self.notify = False

    @classmethod
    def depends(cls,
                user_info: UserInfo = Depends(get_user_info),
                redis: Redis = Depends(get_redis_client),
                main_message: MainMessage = Depends(get_main_message),
                input: str = Depends(get_request_data),
                session: AsyncSession = Depends(session_manager.session),
                ur: UserRepository = Depends(get_user_repo),
                tfr: TariffRepository = Depends(get_tariff_repo),
                sr: ServerRepository = Depends(get_server_repo),
                suir: ServerUserInboundRepository = Depends(
                    get_server_user_inbound_repo),
                psr: PanelServerRepository = Depends(get_panel_server_repo),
                tr: TransactionRepository = Depends(get_transaction_repo)
                ) -> 'Service':
        return cls(user_info, main_message, redis, session, ur, sr, suir, tfr, psr, tr, input)

    async def keyboard_handler(self) -> Output:
        func = self.get_func()
        await func()
        logger.debug(self.input)
        await self.save_main_message()
        return self.output()

    async def chat_handler(self) -> Output:
        return Output(None, None, self.user_info)

    async def start_handler(self) -> Output:
        if await self.ur.get_by_telegram_id(self.user_info.id) is None:
            tariff = (await self.tfr.get_all())[0]
            user = await self.ur.create(self.user_info.id,
                                        self.user_info.username,
                                        self.user_info.lang_code,
                                        "",
                                        tariff.id)
            self.main_message.notifications.append(Notification(
                I18nMessage(MessageKey.welcome_message).render(self.user_info.lang_code)))
            await self.to_main_menu()
        else:
            self.main_message.notifications.append(
                Notification(I18nMessage(MessageKey.dont_use_start_command
                                         ).render(self.user_info.lang_code)))
        await self.save_main_message()
        return self.output()

    def output(self) -> Output:
        rows = [note.text for note in self.main_message.notifications]
        rows += self.main_message.text
        text = "\n".join(rows)
        logger.debug(text)
        if len(self.main_message.notifications) > 0:
            self.main_message.buttons.append(StaticButtons.read_notifications)
        return Output(text, self.main_message.buttons, self.user_info, self.notify)

    async def save_main_message(self) -> None:
        await self.redis.set(f"{RedisType.main_message.value}:{self.user_info.id}",
                             self.main_message.to_str())

    def get_func(self) -> Callable[[], Awaitable[None]]:
        return getattr(self, self.input)

    async def incorrect_input(self) -> None:
        pass

    async def to_main_menu(self) -> None:
        self.main_message.text = [I18nMessage(MessageKey.main_menu
                                              ).render(self.user_info.lang_code)]
        self.main_message.buttons = main_menu_keyboard()

    async def to_inbounds_menu(self) -> None:
        user = await self.ur.get_by_telegram_id(self.user_info.id)
        if user is None:
            raise SendFeedbackToAdminException()
        pservers = await self.psr.get_all()
        inbounds: list[ServerUserInbound] = []
        for pserver in pservers:
            server = pserver.server
            if not server.is_available:
                continue
            inbound = await self.suir.get_by_server_and_user(server, user)
            if len(inbound) == 0:
                async with server_session_manager.get_session(pserver) as session:
                    config = await PanelService(self.session, session
                                                ).get_config(user, AccessType.VLESS_REALITY)
                    if config is None:
                        logger.debug("config is None")
                        continue
                inbound = await self.suir.create(server, user, config)
            else:
                inbound = inbound[0]
            inbounds.append(inbound)
        self.main_message.text = [
            f"```\n{inbound.config.create_string()}\n```" for inbound in inbounds]
        self.main_message.text.append(I18nMessage(MessageKey.inbounds_menu
                                                  ).render(self.user_info.lang_code))
        self.main_message.buttons = inbounds_keyboard()

    async def to_transactions_menu(self) -> None:
        user = await self.ur.get_by_telegram_id(self.user_info.id)
        logger.debug(f"{self.user_info.id} - user tg id")
        if user is None:
            raise SendFeedbackToAdminException()
        trns = await self.tr.get_by_user(user)
        self.main_message.text = [f"{I18nMessage(MessageKey.transactions_menu
                                                 ).render(self.user_info.lang_code
                                                          )}",
                                  f"{I18nMessage(MessageKey.balance
                                                 ).render(self.user_info.lang_code
                                                          )}: {user.balance}"]
        self.main_message.text += [
            f"{trn.amount} - {trn.date}" for trn in trns]
        self.main_message.buttons = transactions_keyboard()

    async def read_notifications(self) -> None:
        self.main_message.notifications.clear()
