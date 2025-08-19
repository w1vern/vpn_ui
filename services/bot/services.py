
from typing import Awaitable, Callable, Protocol
from uuid import UUID

from aiogram import Bot
from fast_depends import Depends
from redis.asyncio import Redis

from ...shared.database.repositories.user import UserRepository
from shared.infrastructure import setup_logger

from .bot import get_bot
from .buttons import (
    Button,
    StaticButtons,
    main_menu_keyboard,
)
from .depends import (
    MainMessage,
    Notification,
    UserInfo,
    get_main_message,
    get_request_data,
    get_state,
    get_user_info,
    get_user_repo
)
from .exceptions import UserNotFoundException
from .redis import RedisType, get_redis_client
from .states import AppStates, MyState

logger = setup_logger(__name__)


class Output:
    def __init__(self,
                 text: str | None,
                 buttons: list[Button] | None,
                 user_info: UserInfo
                 ) -> None:
        self.text = text
        self.buttons = buttons
        self.user_info = user_info


class Service():
    def __init__(self,
                 user_info: UserInfo,
                 state: MyState,
                 main_message: MainMessage,
                 redis: Redis,
                 bot: Bot,
                 ur: UserRepository,
                 input: str
                 ) -> None:
        self.user_info = user_info
        self.state = state
        self.main_message = main_message
        self.redis = redis
        self.bot = bot
        self.ur = ur
        self.input = input

    @classmethod
    def depends(cls,
                user_info: UserInfo = Depends(get_user_info),
                state: MyState = Depends(get_state),
                redis: Redis = Depends(get_redis_client),
                bot: Bot = Depends(get_bot),
                main_message: MainMessage = Depends(get_main_message),
                input: str = Depends(get_request_data),
                ur: UserRepository = Depends(get_user_repo)
                ) -> 'Service':
        return cls(user_info, state, main_message, redis, bot, ur, input)

    async def keyboard_handler(self) -> Output:
        return Output(None, None, self.user_info)

    async def chat_handler(self) -> Output:
        return Output(None, None, self.user_info)

    async def start_handler(self) -> Output:
        if await self.ur.get_by_telegram_id(self.user_info.id) is None:
            user = await self.ur.create(self.user_info.id, self.user_info.username, UUID(int=0))
            self.main_message.notifications.append(Notification("Welcome"))
            await self.__to_main_menu()
        else:
            self.main_message.notifications.append(
                Notification("Don't use start command"))
        await self.__save_main_message()
        return self.__output()

    async def __set_state(self,
                          state: MyState,
                          ) -> None:
        await self.redis.set(f"{RedisType.state.value}:{self.user_info.id}", state.to_str)

    def __output(self) -> Output:
        text = [note.text for note in self.main_message.notifications
                ].append(self.main_message.text)
        return Output(text, self.main_message.buttons, self.user_info)

    async def __save_main_message(self) -> None:
        await self.redis.set(f"{RedisType.main_message.value}:{self.user_info.id}",
                             self.main_message.to_str())

    behavioral_dict: dict[str, str] = {
        f"{AppStates.settings_menu}/{StaticButtons.to_main_menu.text}": "__to_main_menu",
        f"{AppStates.inbounds_menu}/{StaticButtons.to_main_menu.text}": "__to_main_menu"
    }

    async def __get_func(self) -> Callable[[], Awaitable[None]]:
        func = self.behavioral_dict.get(f"{self.state.to_str}/{self.input}")
        if not func:
            func = self.behavioral_dict.get(self.state.to_str)
        if not func:
            func = "__incorrect_input"
        return getattr(self, func)

    async def __incorrect_input(self) -> None:
        pass

    async def __to_main_menu(self) -> None:
        await self.__set_state(AppStates.main_menu)
        self.main_message.text = "main menu"
        self.main_message.buttons = main_menu_keyboard()
