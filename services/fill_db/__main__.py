
import asyncio
from datetime import (
    UTC,
    datetime,
    timedelta,
)
from typing import Any

from sqlalchemy import text

from shared.config import env_config
from shared.database import (
    PanelServerRepository,
    RightsType,
    ServerRepository,
    SettingsType,
    TariffRepository,
    UserRepository,
    session_manager,
)
from shared.infrastructure import setup_logger

logger = setup_logger(__name__)

default_users: list[dict[str, Any]] = [
    {
        "telegram_id": env_config.bot.superuser,
        "telegram_username": "Admin",
        "description": "",
        "balance": 0,
        "rights": RightsType.super_admin.value,
        "settings": SettingsType.default.value,
    }
]

default_tariffs: list[dict[str, Any]] = [
    {
        "name": "default",
        "description": "",
        "duration": timedelta(days=1),
        "price": 3,
        "price_of_traffic_reset": 3,
        "traffic": 50
    }
]

default_servers: list[dict[str, Any]] = [
    {
        "ip": "localhost",
        "description": "",
        "country_code": "ru",
        "is_available": True,
        "display_name": "test",
        "starting_date": datetime.now(UTC).replace(tzinfo=None),
        "closing_date": (datetime.now(UTC) + timedelta(days=365)).replace(tzinfo=None),
    }
]

default_panel_servers: list[dict[str, Any]] = [
    {
        "panel_path": "",
        "login": "admin",
        "password": "admin"
    }
]


async def wait_for_table(table_name: str, retries: int = 30, delay: int = 1) -> None:
    for attempt in range(retries):
        try:
            async with session_manager.context_session() as session:
                result = await session.execute(text("".join([
                    "SELECT 1 ",
                    "FROM information_schema.tables ",
                    "WHERE table_name = :table_name;"
                ])), {"table_name": table_name}
                )
                exists = result.scalar()
                if exists:
                    return
        except Exception as e:
            logger.error(f"[!] Error connecting to DB: {e}")
        logger.info(
            f"[{attempt + 1}/{retries}] Waiting for table '{table_name}'...")
        await asyncio.sleep(delay)
    raise TimeoutError(f"Timed out waiting for table '{table_name}'")


async def main() -> None:
    await wait_for_table("users")
    async with session_manager.context_session() as session:
        ur = UserRepository(session)
        users = await ur.get_all()
        if len(users) > 0:
            logger.info("database is not empty")
            return
        tr = TariffRepository(session)
        _ = None
        for tariff in default_tariffs:
            _ = await tr.create(**tariff)
        if _ is None:
            raise Exception("tariff not created")

        for user in default_users:

            await ur.create(**{
                **user,
                  **{"tariff_id": str(_.id)
                     }})

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

        logger.info("database is filled")

if __name__ == "__main__":
    asyncio.run(main())
