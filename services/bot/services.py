
from typing import Awaitable, Protocol
from aiogram import Bot
from fast_depends import Depends
from redis.asyncio import Redis

from .bot import get_bot

from .buttons import (
    Button,
    StaticButtons,
    main_menu_keyboard,
    settings_keyboard
)
from .depends import (
    UserInfo,
    get_state,
    get_user_info
)
from .redis import RedisType, get_redis_client
from .states import AppStates, MyState


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
                 redis: Redis,
                 bot: Bot
                 ) -> None:
        self.user_info = user_info
        self.state = state
        self.redis = redis
        self.bot = bot

    @classmethod
    def depends(cls,
                user_info: UserInfo = Depends(get_user_info),
                state: MyState = Depends(get_state),
                redis: Redis = Depends(get_redis_client),
                bot: Bot = Depends(get_bot)
                ) -> 'Service':
        return cls(user_info, state, redis, bot)

    async def keyboard_handler(self,
                               input: str
                               ) -> Output:
        pass

    async def chat_handler(self,
                           input: str
                           ) -> Output:
        pass

    async def start_handler(self) -> Output:
        pass

    async def __set_state(self,
                          state: MyState,
                          ) -> None:
        await self.redis.set(f"{RedisType.state}:{self.user_info.id}", state.to_str)

    async def __to_main_menu(self,
                             input: str
                             ) -> Output:
        await self.__set_state(AppStates.main_menu)
        return Output("main menu", main_menu_keyboard(), self.user_info)


async def need_more_buttons_note(message: types.Message,
                                 state: MyState = Depends(get_state)
                                 ) -> None:
    await message.answer(text="chose another button")


async def edit_settings(message: types.Message,
                        redis: Redis = Depends(get_redis_client)
                        ) -> None:
    await state.set_state(AppStates.settings_menu)
    await message.answer(text="use keyboard", reply_markup=settings_keyboard())


async def incorrect_input(message: types.Message,
                          state: MyState = Depends(get_state)
                          ) -> None:
    await message.answer(text="error, use keyboard")


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


behavioral_dict: dict[str, Handler] = {
    f"{AppStates.main_menu.to_str}/{StaticButtons.to_settings_menu.text}": edit_settings,
    f"{AppStates.settings_menu.to_str}": incorrect_input,
    f"{AppStates.settings_menu.to_str}/{StaticButtons.todo_note.text}": need_more_buttons_note,
    f"{AppStates.settings_menu.to_str}/{StaticButtons.to_main_menu.text}": to_main_menu
}
