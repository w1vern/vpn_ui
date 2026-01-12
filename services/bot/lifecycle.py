
from aiogram import Bot, Dispatcher
from fast_depends import Depends, inject

from shared.database import LanguageCodes, UserRepository
from shared.infrastructure import setup_logger

from .bot import update_message
from .depends import get_user_repo
from .i18n import I18nMessage, MessageKey
from .models import Notification, UserInfo
from .service import Service

logger = setup_logger(__name__)


def register_lifecycle(
    dp: Dispatcher,
    bot: Bot
) -> None:
    @dp.startup()
    @inject
    async def on_startup(
        ur: UserRepository = Depends(get_user_repo)
    ) -> None:
        @inject
        async def _(
            user_info: UserInfo,
            service: Service = Depends(Service.depends)
        ) -> None:
            service.main_message.notifications.append(
                Notification(I18nMessage(MessageKey.bot_started
                                         ).render(service.user_info.lang_code)))
            await service.save_main_message()
            service.notify = True
            await update_message(service.output())
        users = await ur.get_all()
        for user in users:
            await _(UserInfo(
                id=user.telegram_id,
                username=user.telegram_username,
                lang_code=LanguageCodes(user.settings.language_code)
            ))

    @dp.shutdown()
    @inject
    async def on_shutdown(
        ur: UserRepository = Depends(get_user_repo)
    ) -> None:
        @inject
        async def _(
            user_info: UserInfo,
            service: Service = Depends(Service.depends)
        ) -> None:
            text = I18nMessage(MessageKey.bot_stopped).render(
                service.user_info.lang_code)
            service.main_message.notifications.append(Notification(text))
            await service.save_main_message()
            service.notify = True
            output = service.output()
            output.buttons = []
            output.text = text
            await update_message(output)
        users = await ur.get_all()
        for user in users:
            await _(UserInfo(
                id=user.telegram_id,
                username=user.telegram_username,
                lang_code=LanguageCodes(user.settings.language_code)
            ))
