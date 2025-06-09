import asyncio
from datetime import UTC, datetime, timedelta

from shared.database import (PanelServer, PanelServerRepository, RightsType,
                             Server, ServerRepository, SettingsType,
                             TariffRepository, User, UserRepository,
                             session_manager)
from shared.database.enums.rights_type import RightsType
from shared.database.enums.settings_type import SettingsType


async def main():
    async with session_manager.context_session() as session:
        sr = ServerRepository(session)
        psr = PanelServerRepository(session)
        ur = UserRepository(session)
        tr = TariffRepository(session)
        s = await sr.create(
            ip="3xui.demogram.ru",
            country_code="ru",
            display_name="1",
            is_available=True,
            starting_date=datetime.now(UTC).replace(tzinfo=None),
            closing_date=(datetime.now(UTC) + timedelta(days=30)).replace(tzinfo=None))
        ps = await psr.create(
            server=s,
            panel_path="",
            login="admin",
            password="admin",
            vless_id=0,
            vless_reality_id=0,
            vmess_id=0)
        t = await tr.create(
            name="default",
            duration=timedelta(days=1),
            price=3,
            price_of_traffic_reset=3,
            traffic=50
        )
        user = await ur.create(
            telegram_id=101,
            telegram_username="aboba1",
            balance=0,
            rights=RightsType.super_admin.value,
            settings=SettingsType.default.value,
            tariff_id=t.id)


if __name__ == "__main__":
    asyncio.run(main())
