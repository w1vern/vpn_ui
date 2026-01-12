
from fast_depends import Depends, inject
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import (
    LanguageCodes,
    UserRepository,
    session_manager
)
from shared.infrastructure import (
    RABBIT_URL,
    CodeToTG,
    NotificationToTG,
    notification_queue,
    setup_logger,
    tg_code_queue
)

from .bot import update_message
from .i18n import I18nMessage, MessageKey
from .models import Notification, UserInfo
from .service import Service

logger = setup_logger(__name__)

broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)


@broker.subscriber(queue=tg_code_queue)
async def handle_tg_code(data: CodeToTG) -> None:
    @inject
    async def _(
        text: str,
        user_info: UserInfo,
        service: Service = Depends(Service.depends)
    ) -> None:
        service.main_message.notifications.append(Notification(text))
        await service.save_main_message()
        service.notify = True
        await update_message(service.output())
    await _(
        text=I18nMessage(MessageKey.telegram_code).render(
            data.lang_code, code=data.code),
        user_info=UserInfo(data.id, data.username, data.lang_code)
    )


@broker.subscriber(queue=notification_queue)
async def handle_notification(data: NotificationToTG) -> None:
    @inject
    async def _(
        text: str,
        notify: bool,
        user_info: UserInfo,
        session: AsyncSession,
        service: Service = Depends(Service.depends)
    ) -> None:
        service.main_message.notifications.append(Notification(text))
        await service.save_main_message()
        service.notify = notify
        await update_message(service.output())
    logger.debug(data)
    async with session_manager.context_session() as session:
        ur = UserRepository(session)
        users = await ur.get_all()
        for user in users:
            lang_code = LanguageCodes(user.settings.language_code)
            text = data.data.get(
                lang_code,
                data.data[LanguageCodes.en]
            )
            user_info = UserInfo(
                id=user.telegram_id,
                username=user.telegram_username,
                lang_code=lang_code
            )
            await _(
                text=text,
                notify=data.notify,
                user_info=user_info,
                session=session
            )
