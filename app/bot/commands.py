
from app.database.repositories.user_repository import UserRepository
from app.database.database import sessionmanager
from app.bot.main import bot
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message
import functools

def session_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        with sessionmanager.session() as session:
            return func(session, *args, **kwargs)
        return wrapper
    
@session_decorator
async def start_command(session: AsyncSession, message: Message):
    ur = UserRepository(session)
    



async def send_message(telegram_id, message):
    await bot.send_message(chat_id=telegram_id, text=message)