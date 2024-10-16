
from app.database.repositories import *
from app.database.enums import *
from app.database.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message
from app.bot.di_implementation import inject, di
from app.bot.static.message_title import MessageTitle
from app.bot.static.template_title import TemplateTitle
from app.bot.static.types import *
from telebot.async_telebot import AsyncTeleBot
from string import Template
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

@inject(di)
async def string_builder(template_title: TemplateTitle, language_code: str, **kwargs) -> str:
    template = Template(templates[template_title])
    if language_code == 'ru':
        return template.substitute(ru_messages, **kwargs)
    return template.substitute(en_messages, **kwargs)


@inject(di)
async def start_command(message: Message, user: User, bot: AsyncTeleBot):
    text = string_builder(template_title=TemplateTitle.start_message, )
    await bot.send_message(message.from_user.id, )


@inject(di)
async def toggle_auto_pay_command(user: User, session: AsyncSession, bot: AsyncTeleBot, templates: Templates, ru_messages: RuMessages, en_messages: EnMessages):
    ur = UserRepository(session)
    await ur.toggle_auto_pay(user)
    await session.commit()



