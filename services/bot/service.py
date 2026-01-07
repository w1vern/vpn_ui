
from collections.abc import Awaitable, Callable
from uuid import UUID

from fast_depends import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    DefaultTariffs,
    ServerInboundRepository,
    ServerRepository,
    TariffRepository,
    TransactionRepository,
    UserRepository,
    session_manager
)
from shared.infrastructure import env_config, setup_logger

from .buttons import (
    StaticButtons,
    inbounds_keyboard,
    main_menu_keyboard,
    transactions_keyboard
)
from .depends import (
    get_main_message,
    get_request_data,
    get_server_inbound_repo,
    get_server_repo,
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
    def __init__(
        self,
        user_info: UserInfo,
        main_message: MainMessage,
        redis: Redis,
        session: AsyncSession,
        ur: UserRepository,
        sr: ServerRepository,
        tfr: TariffRepository,
        sir: ServerInboundRepository,
        tr: TransactionRepository,
        input: str
    ) -> None:
        self.user_info = user_info
        self.main_message = main_message
        self.redis = redis
        self.session = session
        self.ur = ur
        self.sr = sr
        self.tfr = tfr
        self.sir = sir
        self.tr = tr
        self.input = input

        self.notify = False

    @classmethod
    def depends(
        cls,
        user_info: UserInfo = Depends(get_user_info),
        redis: Redis = Depends(get_redis_client),
        main_message: MainMessage = Depends(get_main_message),
        input: str = Depends(get_request_data),
        session: AsyncSession = Depends(session_manager.session),
        ur: UserRepository = Depends(get_user_repo),
        tfr: TariffRepository = Depends(get_tariff_repo),
        sr: ServerRepository = Depends(get_server_repo),
        sir: ServerInboundRepository = Depends(get_server_inbound_repo),
        tr: TransactionRepository = Depends(get_transaction_repo)
    ) -> 'Service':
        return cls(
            user_info=user_info,
            main_message=main_message,
            redis=redis,
            session=session,
            ur=ur,
            sr=sr,
            tfr=tfr,
            sir=sir,
            tr=tr,
            input=input
        )

    async def keyboard_handler(self) -> Output:
        func = self.get_func()
        await func()
        await self.save_main_message()
        return self.output()

    async def chat_handler(self) -> Output:
        return Output(
            text=None,
            buttons=None,
            user_info=self.user_info,
            notify=False
        )

    async def start_handler(self) -> Output:
        if await self.ur.get_by_telegram_id(self.user_info.id) is None:
            tariff = await self.tfr.get_by_id(UUID(int=DefaultTariffs.DEFAULT.value))
            if tariff is None:
                raise SendFeedbackToAdminException()
            await self.ur.create(
                telegram_id=self.user_info.id,
                telegram_username=self.user_info.username,
                telegram_language_code=self.user_info.lang_code,
                description="",
                tariff=tariff,
                internal_id=str(self.user_info.id),
            )
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
        if len(self.main_message.notifications) > 0:
            self.main_message.buttons.append(StaticButtons.read_notifications)

        return Output(text, self.main_message.buttons, self.user_info, self.notify)

    async def save_main_message(self) -> None:
        await self.redis.set(
            f"{RedisType.main_message.value}:{self.user_info.id}",
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
        self.main_message.text = [
            f"<code>{env_config.backend.url}/sub/{user.panel_id}</code>"
        ]
        self.main_message.text.append(I18nMessage(
            MessageKey.inbounds_menu
        ).render(self.user_info.lang_code))
        self.main_message.buttons = inbounds_keyboard()

    async def to_transactions_menu(self) -> None:
        user = await self.ur.get_by_telegram_id(self.user_info.id)
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
