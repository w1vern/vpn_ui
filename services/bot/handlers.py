
from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, ErrorEvent, Message
from fast_depends import Depends, inject

from shared.infrastructure import setup_logger
from shared.database import LanguageCodes

from .bot import update_message
from .exceptions import (
    BaseCustomException,
    MessageTextIsNoneException,
    SendFeedbackToAdminException
)
from .i18n import I18nMessage as MyMessage
from .i18n import MessageKey
from .models import UserInfo
from .service import Output, Service

logger = setup_logger(__name__)

router = Router()


@router.message(Command("start"))
@inject
async def cmd_start(message: Message,
                    service: Service = Depends(Service.depends)
                    ) -> None:
    await message.delete()
    await update_message(await service.start_handler())


@router.message()
@inject
async def handle_text(message: Message,
                      service: Service = Depends(Service.depends)
                      ) -> None:
    await message.delete()
    if message.text is None:
        raise MessageTextIsNoneException()
    await update_message(await service.chat_handler())


@router.callback_query()
@inject
async def handle_inline_button(callback_query: CallbackQuery,
                               service: Service = Depends(Service.depends)
                               ) -> None:
    if callback_query.data is None:
        raise MessageTextIsNoneException()
    logger.debug(callback_query.data)
    await update_message(await service.keyboard_handler())


# @router.errors()
async def error_handler(event: ErrorEvent) -> None:
    exception = event.exception
    if event.update.message is None:
        if event.update.callback_query is None \
                or event.update.callback_query.from_user is None \
                or event.update.callback_query.from_user.username is None \
                or event.update.callback_query.from_user.language_code is None:
            raise SendFeedbackToAdminException()
        id = event.update.callback_query.from_user.id
        username = event.update.callback_query.from_user.username
        lang_code = LanguageCodes(event.update.callback_query.from_user.language_code)
    else:
        if event.update.message.from_user is None \
                or event.update.message.from_user.username is None\
                    or event.update.message.from_user.language_code is None:
            raise SendFeedbackToAdminException()
        id = event.update.message.from_user.id
        username = event.update.message.from_user.username
        lang_code = LanguageCodes(event.update.message.from_user.language_code)
    user_info = UserInfo(id, username, lang_code)
    new_state = Output(None, None, user_info)
    if event.update.message is None \
            or event.update.message.from_user is None \
            or event.update.message.from_user.language_code is None:
        lang_code = LanguageCodes.en
    else:
        lang_code = LanguageCodes(event.update.message.from_user.language_code)
    if isinstance(exception, BaseCustomException):
        new_state.text = exception.detail.render(lang_code)
    elif isinstance(exception, TelegramAPIError):
        new_state.text = MyMessage(MessageKey.telegram_api_error).render(lang_code)
    else:
        new_state.text = MyMessage(MessageKey.unknown_error).render(lang_code)
    await update_message(new_state)
    raise exception
