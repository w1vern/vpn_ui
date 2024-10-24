
from app.database.repositories import *
from app.database.enums import *
from app.database.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from telebot.types import Message
from app.bot.di_implementation import inject, di
from app.bot.static.message_title import MessageTitle
from app.bot.static.template_title import TemplateTitle
from telebot.async_telebot import AsyncTeleBot
from string import Template
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from app.bot.main import ru_messages, en_messages, templates

async def string_builder(template_title: TemplateTitle, language_code: str, **kwargs) -> str:
    template = Template(templates[template_title.value])
    if language_code == 'ru':
        return template.substitute(ru_messages, **kwargs)
    return template.substitute(en_messages, **kwargs)


@inject(di)
async def start_command(message: Message, user: User, bot: AsyncTeleBot):
    text = await string_builder(template_title=TemplateTitle.start_template, language_code=message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)
    print(message.chat.id)


@inject(di)
async def toggle_auto_pay_command(message: Message, user: User, session: AsyncSession, bot: AsyncTeleBot):
    ur = UserRepository(session)
    await ur.toggle_auto_pay(user)
    await session.commit()
    text = string_builder(TemplateTitle.toggle_auto_pay_template, message.from_user.language_code)
    bot.send_message(message.from_user.id, text)
""" 
@inject
async def info_command(message: Message, user: User, bot: AsyncTeleBot):
    text = string_builder(TemplateTitle.info_template, message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)

@inject
async def help_command(message: Message, user: User, bot: AsyncTeleBot):
    text = string_builder(TemplateTitle.help_template, message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)

@inject
async def problem_command(message: Message, user: User, bot: AsyncTeleBot):
    text = string_builder(TemplateTitle.problem_template, message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)

@inject
async def get_my_connections_command(message: Message, user: User, bot: AsyncTeleBot):
    text = string_builder(TemplateTitle.my_connections, message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)

@inject
async def _command(message: Message, user: User, bot: AsyncTeleBot):
    pass


 """