
from app.database.database import get_db_session
from app.database.repositories import *
from app.database.enums import *
from app.database.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message
from app.bot.container import inject, di
from app.bot.main import bot, static_messages
from app.bot.static.messages_titles import MessageTitle



@inject(di)
async def start_command(message: Message, user: User):
    await bot.send_message(message.from_user.id, static_messages[MessageTitle.start_message])


@di.inject
async def installation_command(user: User, session: AsyncSession, message: Message):
    pass


