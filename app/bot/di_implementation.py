import functools
from telebot.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.async_telebot import AsyncTeleBot


from app.bot.di_container import Container, RequestContext
from app.database.database import get_db_session
from app.database.repositories import *
from app.database.models import *
from app.bot.main import bot, ru_messages, en_messages, templates


di = Container()


def request_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rq = RequestContext()
        rq.set_depend(Message, args[0])
        return func(rq)
    return wrapper


def inject(di):
    def decorator(func):
        return request_decorator(di.inject(func))
    return decorator


@di.inject
#@inject(di)
async def get_user(session: AsyncSession, message: Message):
    ur = UserRepository(session)
    user = await ur.get_by_telegram_id(message.from_user.id)
    if user is None:
        user = await ur.create(telegram_id=message.from_user.id,
                               telegram_username=message.from_user.username)
        await session.commit()
    return user


async def get_bot():
    return bot


di.set_depend(AsyncSession, get_db_session)
di.set_depend(User, get_user)
di.set_depend(AsyncTeleBot, get_bot)
