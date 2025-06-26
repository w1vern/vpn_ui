
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

#from .services import get_func, to_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message,
                    state: FSMContext,
                    ) -> None:
    await message.answer(f"hello, your rank: {user.rank}")
    await to_main_menu(message, state, user, session)


@router.message()
async def handle_button(message: types.Message,
                        state: FSMContext,
                        ) -> None:
    await get_func(
        await state.get_state(),
        message.text)(message,
                      state,
                      user,
                      session)
