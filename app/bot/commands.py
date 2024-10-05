
from app.database.repositories import *
from app.database.enums import *
from app.database.database import sessionmanager
from app.bot.__main__ import bot
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message
import functools

from app.bot.main import static_messages
from app.bot.static.messages_titles import MessageTitle

async def user_exists(session: AsyncSession, message: Message) -> bool:
    ur = UserRepository()
    if await ur.get_by_telegram_id(message.from_user.id):
        return True
    return False

async def user_with_rights(session: AsyncSession, message: Message) -> bool:
    ur = UserRepository()
    if not (await ur.get_by_telegram_id(message.from_user.id)).role == Role.guest:
        return True
    return False

def session_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        with sessionmanager.session() as session:
            return func(session, *args, **kwargs)
        return wrapper
    
@session_decorator
async def start_command(session: AsyncSession, message: Message):
    ur = UserRepository(session)
    ur.create(telegram_id=message.from_user.id, telegram_username=message.from_user.username)
    bot.reply_to(message, static_messages[MessageTitle.start_message])

@session_decorator
async def installation_command(session: AsyncSession, message: Message):
    pass
    



async def send_message(telegram_id, message):
    await bot.send_message(chat_id=telegram_id, text=message)