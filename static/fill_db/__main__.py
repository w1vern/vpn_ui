
import asyncio
import os
import secrets
from datetime import UTC, datetime

from dotenv import load_dotenv

from database.database import session_manager
from database.enums.rights_type import RightsType
from database.models.user import User
from database.repositories import UserRepository

load_dotenv()

SUPERUSER_TELEGRAM_ID = os.getenv("SUPERUSER_TELEGRAM_ID")

if SUPERUSER_TELEGRAM_ID is None:
    raise Exception()

default_users = [{
    "telegram_id": int(SUPERUSER_TELEGRAM_ID), "telegram_username": "Admin", "balance": 0, "role": RightsType.super_admin,
    "active": True, "auto_pay": False, "created_date": datetime.now(UTC).replace(tzinfo=None), "secret": secrets.token_urlsafe()
}]


async def main():
    async with session_manager.session() as session:
        ur = UserRepository(session)
        for user in default_users:
            await ur.create(**user)


if __name__ == "__main__":
    asyncio.run(main())
