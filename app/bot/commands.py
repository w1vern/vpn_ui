
from app.database.repositories import *
from app.database.database import sessionmanager
from app.bot.__main__ import bot
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message
import functools

from app.bot.main import static_messages
from app.bot.static.messages_titles import MessageTitle

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
    



async def send_message(telegram_id, message):
    await bot.send_message(chat_id=telegram_id, text=message)