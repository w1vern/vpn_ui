
import asyncio
from datetime import timedelta

from sqlalchemy import text

from shared.database import (
    TariffRepository,
    UserRepository,
    UserRights,
    UserSettings,
    session_manager
)
from shared.infrastructure import env_config, setup_logger

logger = setup_logger(__name__)


async def wait_for_table(
    table_name: str,
    retries: int = 30,
    delay: int = 1
) -> None:
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
        tr = TariffRepository(session)
        users = await ur.get_all()
        if len(users) > 0:
            logger.info("database is not empty")
            return
        tariff = await tr.create(
            name="__default_tariff__",
            description="Default tariff. Equals to no tariff.",
            price=0,
            price_of_traffic_reset=0,
            traffic=0,
            duration=timedelta(seconds=0),
            with_access=False,
            with_unavailable_inbounds=False,
            is_special=True
        )
        user = await ur.create(
            telegram_id=env_config.bot.superuser,
            telegram_username="super-admin",
            description="First user, super-admin",
            balance=0,
            tariff=tariff,
            rights=UserRights(),
            settings=UserSettings(),
            internal_id="super-admin"
        )
        await ur.update_rights(
            user=user,
            is_admin_rights_editor=True,
            is_member_rights_editor=True,
            is_users_editor=True,
            is_servers_editor=True,
            is_control_panel_user=True,
            is_transactions_editor=True,
            is_verified=True,
            is_tariffs_editor=True
        )
        logger.info("database is filled")

if __name__ == "__main__":
    asyncio.run(main())
