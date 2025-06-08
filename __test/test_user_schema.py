




import asyncio

from back.schemas.user import UserSchema
from infra.database.main import session_manager
from infra.database.repositories.user_repository import UserRepository


async def main():
    async with session_manager.session() as session:
        ur = UserRepository(session)
        user = await ur.get_by_telegram_id("532109910")
        us = UserSchema.from_db(user)
        print(user.rights)
        print(us)
        print(getattr(user, "is_control_panel_user"))
        print(user.is_control_panel_user)


asyncio.run(main())
