
from typing import Awaitable, Protocol

from aiogram import Bot
from fast_depends import Depends
from redis.asyncio import Redis

from shared.infrastructure import setup_logger

from .bot import get_bot
from .buttons import (
    Button,
    StaticButtons,
    main_menu_keyboard,
)
from .depends import (
    MainMessage,
    UserInfo,
    get_main_message,
    get_state,
    get_user_info
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


class Handler(Protocol):
    def __call__(self,
                 input: str,
                 ) -> Awaitable[Output]:
        ...


class Service():
    def __init__(self,
                 user_info: UserInfo,
                 state: MyState,
                 main_message: MainMessage,
                 redis: Redis,
                 bot: Bot
                 ) -> None:
        self.user_info = user_info
        self.state = state
        self.main_message = main_message
        self.redis = redis
        self.bot = bot

    @classmethod
    def depends(cls,
                user_info: UserInfo = Depends(get_user_info),
                state: MyState = Depends(get_state),
                redis: Redis = Depends(get_redis_client),
                bot: Bot = Depends(get_bot),
                main_message: MainMessage = Depends(get_main_message)
                ) -> 'Service':
        return cls(user_info, state, main_message, redis, bot)

    async def keyboard_handler(self,
                               input: str
                               ) -> Output:
        return Output(None, None, self.user_info)

    async def chat_handler(self,
                           input: str
                           ) -> Output:
        return Output(None, None, self.user_info)

    async def start_handler(self) -> Output:
        raise UserNotFoundException()

    async def __set_state(self,
                          state: MyState,
                          ) -> None:
        await self.redis.set(f"{RedisType.state.value}:{self.user_info.id}", state.to_str)

    async def __set_main_message(self,
                                 output: Output
                                 ) -> None:
        await self.redis.set(f"{RedisType.main_message.value}:{self.user_info.id}",
                             MainMessage(
                                 id=self.main_message.id,
                                 text=self.main_message.text if output.text is None else output.text,
                                 buttons=self.main_message.buttons if output.buttons is None else output.buttons
        ).to_str())

    async def __to_main_menu(self,
                             input: str
                             ) -> Output:
        await self.__set_state(AppStates.main_menu)
        return Output("main menu", main_menu_keyboard(), self.user_info)

    async def __get_func(self) -> Handler:
        pass

    async def edit_settings(self, input: str) -> Output:
        pass

    async def incorrect_input(self, input: str) -> Output:
        pass

    async def need_more_buttons_note(self, input: str) -> Output:
        pass

    async def to_main_menu(self, input: str) -> Output:
        pass

    behavioral_dict: dict[str, Handler] = {
        f"{AppStates.main_menu.to_str}/{StaticButtons.to_settings_menu.text}": edit_settings,
        f"{AppStates.settings_menu.to_str}": incorrect_input,
        f"{AppStates.settings_menu.to_str}/{StaticButtons.todo_note.text}": need_more_buttons_note,
        f"{AppStates.settings_menu.to_str}/{StaticButtons.to_main_menu.text}": to_main_menu
    }


"""
def get_func(current_state: str | None,
             message: str | None
             ) -> Handler:
    if not current_state:
        raise Exception("current state is None")
    if not message:
        raise Exception("message is None")
    func = behavioral_dict.get(f"{current_state}/{message}")
    if not func:
        func = behavioral_dict.get(current_state)
    if not func:
        func = incorrect_input
    return func
"""
