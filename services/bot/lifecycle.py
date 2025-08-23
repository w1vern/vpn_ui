
from aiogram import Bot, Dispatcher
from fast_depends import Depends, inject

from shared.database import UserRepository
from shared.infrastructure import setup_logger

from .bot import update_message
from .depends import get_user_repo
from .models import Notification
from .services import Service

logger = setup_logger(__name__)


def register_lifecycle(dp: Dispatcher,
                       bot: Bot
                       ) -> None:
    @dp.startup()
    @inject
    async def on_startup(ur: UserRepository = Depends(get_user_repo)
                         ) -> None:
        @inject
        async def _(id: int,
                    service: Service = Depends(Service.depends)
                    ) -> None:
            service.main_message.notifications.append(
                Notification("bot startup"))
            await service.save_main_message()
            service.notify = True
            await update_message(service.output())
        users = await ur.get_all()
        for user in users:
            await _(user.telegram_id)

    @dp.shutdown()
    @inject
    async def on_shutdown(ur: UserRepository = Depends(get_user_repo)
                          ) -> None:
        @inject
        async def _(id: int,
                    service: Service = Depends(Service.depends)
                    ) -> None:
            service.main_message.notifications.append(
                Notification("bot shutdown"))
            await service.save_main_message()
            service.notify = True
            await update_message(service.output())
        users = await ur.get_all()
        for user in users:
            await _(user.telegram_id)
