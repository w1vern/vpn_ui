
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InaccessibleMessage, Message

from .services import get_func, to_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message,
                    state: FSMContext,
                    ) -> None:
    await message.delete()
    await to_main_menu(message, state)


@router.message()
async def handle_text(message: Message,
                      state: FSMContext,
                      ) -> None:
    await message.delete()


@router.callback_query()
async def handle_inline_button(callback_query: CallbackQuery,
                               state: FSMContext,
                               ) -> None:
    if callback_query.message is None \
            or isinstance(callback_query.message, InaccessibleMessage):
        return
    await get_func(
        await state.get_state(), callback_query.data)(
            callback_query.message,
            state
    )
