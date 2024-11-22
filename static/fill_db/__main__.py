
import asyncio
import os
import secrets
from datetime import UTC, datetime

from dotenv import load_dotenv

from database.database import session_manager
from database.enums.role import Role
from database.models.user import User
from database.repositories import UserRepository

load_dotenv()

SUPERUSER_TELEGRAM_ID = os.getenv("SUPERUSER_TELEGRAM_ID")

default_users = [{
    "telegram_id": int(SUPERUSER_TELEGRAM_ID), "telegram_username": "Admin", "balance": 0, "role": Role.admin,
    "active": True, "auto_pay": False, "created_date": datetime.now(UTC).replace(tzinfo=None), "secret": secrets.token_urlsafe()
}]


async def main():
    async with session_manager.session() as session:
        ur = UserRepository(session)
        for user in default_users:
            await ur.create(**user)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
