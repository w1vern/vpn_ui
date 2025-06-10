




import asyncio

from config import settings
from services.backend.schemas import UserSchema
from shared.database import UserRepository, session_manager


async def main():
    async with session_manager.context_session() as session:
        ur = UserRepository(session)
        user = await ur.get_by_telegram_id(settings.bot.superuser)
        if user is None:
            raise Exception("user not found")
        us = UserSchema.from_db(user)
        print(user.rights)
        print(us)
        print(getattr(user, "is_control_panel_user"))
        print(user.is_control_panel_user)


asyncio.run(main())
