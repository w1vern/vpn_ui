
import asyncio
import os
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

from dotenv import load_dotenv

from database.database import session_manager
from database.enums.rights_type import RightsType
from database.enums.settings_type import SettingsType
from database.models.tariff import Tariff
from database.models.user import User
from database.repositories import UserRepository, TariffRepository

load_dotenv()

SUPERUSER_TELEGRAM_ID = os.getenv("SUPERUSER_TELEGRAM_ID")

if SUPERUSER_TELEGRAM_ID is None:
    raise Exception()

default_users = [{
    "telegram_id": SUPERUSER_TELEGRAM_ID,
    "telegram_username": "Admin",
    "balance": 0,
    "rights": RightsType.super_admin.value,
    "settings": SettingsType.default.value,
    "created_date": datetime.now(UTC).replace(tzinfo=None),
    "secret": secrets.token_urlsafe()
}]

default_tariffs = [
    {
        "name": "default",
        "duration": timedelta(days=1),
        "price": 3,
        "price_of_traffic_reset": 3,
        "traffic": 50
    }
]


async def main():
    async with session_manager.session() as session:
        tr = TariffRepository(session)
        _ = None
        for tariff in default_tariffs:
            _ = await tr.create(**tariff)

        if _ is None:
            raise Exception()
        
        ur = UserRepository(session)
        for user in default_users:
            await ur.create(**{**user,  **{"tariff_id": str(_.id)}})


if __name__ == "__main__":
    asyncio.run(main())
