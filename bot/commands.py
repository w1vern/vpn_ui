
from string import Template

from sqlalchemy.ext.asyncio import AsyncSession
from telebot.async_telebot import AsyncTeleBot
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from bot.di_implementation import di, inject
from bot.main import en_messages, ru_messages, templates
from bot.static.message_title import MessageTitle
from bot.static.template_title import TemplateTitle
from database.enums import *
from database.models import *
from database.repositories import *


async def string_builder(template_title: TemplateTitle, language_code: str | None, **kwargs) -> str:
    template = Template(templates[template_title.value])
    if language_code == "ru":
        return template.substitute(ru_messages, **kwargs)
    return template.substitute(en_messages, **kwargs)


@inject(di)
async def start_command(message: Message, user: User, bot: AsyncTeleBot):
    if message.from_user is None:
        return
    text = await string_builder(template_title=TemplateTitle.start_template, language_code=message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)


@inject(di)
async def toggle_auto_pay_command(message: Message, user: User, session: AsyncSession, bot: AsyncTeleBot):
    if message.from_user is None:
        return
    ur = UserRepository(session)
    await ur.toggle_auto_pay(user)
    text = await string_builder(TemplateTitle.toggle_auto_pay_template, message.from_user.language_code)
    await bot.send_message(message.from_user.id, text)
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
