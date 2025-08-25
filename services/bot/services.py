
from typing import Awaitable, Callable
from uuid import UUID

from fast_depends import Depends
from redis.asyncio import Redis

from shared.database import (
    PanelServerRepository,
    ServerRepository,
    TransactionRepository,
    UserRepository
)
from shared.infrastructure import setup_logger

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
    get_state,
    get_transaction_repo,
    get_user_info,
    get_user_repo
)
from .exceptions import SendFeedbackToAdminException
from .models import MainMessage, Notification, Output, UserInfo
from .redis import RedisType, get_redis_client
from .states import AppStates, MyState

logger = setup_logger(__name__)


class Service():
    def __init__(self,
                 user_info: UserInfo,
                 state: MyState,
                 main_message: MainMessage,
                 redis: Redis,
                 ur: UserRepository,
                 sr: ServerRepository,
                 psr: PanelServerRepository,
                 tr: TransactionRepository,
                 input: str
                 ) -> None:
        self.user_info = user_info
        self.state = state
        self.main_message = main_message
        self.redis = redis
        self.ur = ur
        self.sr = sr
        self.psr = psr
        self.tr = tr
        self.input = input

        self.notify = False

    @classmethod
    def depends(cls,
                user_info: UserInfo = Depends(get_user_info),
                state: MyState = Depends(get_state),
                redis: Redis = Depends(get_redis_client),
                main_message: MainMessage = Depends(get_main_message),
                input: str = Depends(get_request_data),
                ur: UserRepository = Depends(get_user_repo),
                sr: ServerRepository = Depends(get_server_repo),
                psr: PanelServerRepository = Depends(get_panel_server_repo),
                tr: TransactionRepository = Depends(get_transaction_repo)
                ) -> 'Service':
        return cls(user_info, state, main_message, redis, ur, sr, psr, tr, input)

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
            user = await self.ur.create(self.user_info.id, self.user_info.username, UUID(int=0))
            self.main_message.notifications.append(Notification("Welcome"))
            await self.to_main_menu()
        else:
            self.main_message.notifications.append(
                Notification("Don't use start command"))
        await self.save_main_message()
        return self.output()

    async def set_state(self,
                        state: MyState,
                        ) -> None:
        await self.redis.set(f"{RedisType.state.value}:{self.user_info.id}", state.to_str)

    def output(self) -> Output:
        notes = [note.text for note in self.main_message.notifications]
        notes.append(self.main_message.text)
        text = "\n".join(notes)
        return Output(text, self.main_message.buttons, self.user_info, self.notify)

    async def save_main_message(self) -> None:
        await self.redis.set(f"{RedisType.main_message.value}:{self.user_info.id}",
                             self.main_message.to_str())

    behavioral_dict: dict[str, str] = {
        # f"{AppStates.settings_menu}/{StaticButtons.to_main_menu.text}": "__to_main_menu",
        f"{AppStates.inbounds_menu}/{StaticButtons.to_main_menu.text}": "to_main_menu",
        f"{AppStates.transactions_menu}/{StaticButtons.to_main_menu.text}": "to_main_menu",
        f"{AppStates.main_menu}/{StaticButtons.to_inbounds_menu.text}": "to_inbounds_menu",
        f"{AppStates.main_menu}/{StaticButtons.to_transactions_menu.text}": "to_transactions_menu",
    }

    def get_func(self) -> Callable[[], Awaitable[None]]:
        func = self.behavioral_dict.get(f"{self.state.to_str}/{self.input}")
        if not func:
            func = self.behavioral_dict.get(self.state.to_str)
        if not func:
            func = "incorrect_input"
        logger.debug(func)
        return getattr(self, func)

    async def incorrect_input(self) -> None:
        pass

    async def to_main_menu(self) -> None:
        await self.set_state(AppStates.main_menu)
        self.main_message.text = "main menu"
        self.main_message.buttons = main_menu_keyboard()

    async def to_inbounds_menu(self) -> None:
        await self.set_state(AppStates.inbounds_menu)
        self.main_message.text = "inbounds menu"
        self.main_message.buttons = inbounds_keyboard()

    async def to_transactions_menu(self) -> None:
        await self.set_state(AppStates.transactions_menu)
        user = await self.ur.get_by_telegram_id(self.user_info.id)
        if user is None:
            raise SendFeedbackToAdminException()
        trns = await self.tr.get_by_user(user)
        text = "\n".join([f"{trn.amount} - {trn.date}" for trn in trns])
        self.main_message.text = f"transactions menu\nbalance: {user.balance}\n{text}"
        self.main_message.buttons = transactions_keyboard()
