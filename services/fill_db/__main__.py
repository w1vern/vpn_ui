
import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from config import settings
from infra.database.enums import RightsType, SettingsType
from infra.database.main import session_manager
from infra.database.repositories import (PanelServerRepository, ServerRepository,
                                   TariffRepository, UserRepository)

default_users = [{
    "telegram_id": settings.superuser_telegram_id,
    "telegram_username": "Admin",
    "balance": 0,
    "rights": RightsType.super_admin.value,
    "settings": SettingsType.default.value,
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

default_servers = [
    {
        "ip": "localhost",
        "country_code": "ru",
        "is_available": True,
        "display_name": "test",
        "starting_date": datetime.now(UTC).replace(tzinfo=None),
        "closing_date": (datetime.now(UTC) + timedelta(days=365)).replace(tzinfo=None),
    }
]

default_panel_servers = [
    {
        "panel_path": "",
        "login": "admin",
        "password": "admin"
    }
]


async def main() -> None:
    async with session_manager.context_session() as session:
        ur = UserRepository(session)
        users = await ur.get_all()
        if len(users) > 0:
            raise Exception("database is not empty")
        tr = TariffRepository(session)
        _ = None
        for tariff in default_tariffs:
            _ = await tr.create(**tariff)
        if _ is None:
            raise Exception("tariff not created")

        for user in default_users:
            await ur.create(**{**user,  **{"tariff_id": str(_.id)}})

        sr = ServerRepository(session)
        psr = PanelServerRepository(session)
        for i in range(len(default_servers)):
            server = await sr.create(**default_servers[i])
            pserver = default_panel_servers[i]
            await psr.create(
                server=server,
                panel_path=pserver["panel_path"],
                login=pserver["login"],
                password=pserver["password"])

if __name__ == "__main__":
    asyncio.run(main())
