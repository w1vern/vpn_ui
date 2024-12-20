import asyncio
import secrets
from datetime import UTC, datetime, timedelta

from database.database import session_manager
from database.models.panel_server import PanelServer
from database.models.server import Server
from database.models.user import User
from database.repositories.panel_server_repository import PanelServerRepository
from database.repositories.user_repository import UserRepository


async def main():
    async with session_manager.session() as session:
        psr = PanelServerRepository(session)
        ur = UserRepository(session)
        ps = await psr.create(ip="3xui.demogram.ru", country_code="ru", display_name="1",
                is_available=True, created_date=datetime.now(UTC).replace(tzinfo=None), closing_date=(datetime.now(UTC) + timedelta(days=30)).replace(tzinfo=None), panel_path="", login="admin", password="admin", vless_id=0, vless_reality_id=0, vmess_id=0)
        user = await ur.create(telegram_id=101, telegram_username="aboba1", balance=0, role=Role.admin, active=True,
           auto_pay=False, created_date=datetime.now(UTC).replace(tzinfo=None), secret=secrets.token_urlsafe())
        

if __name__ == "__main__":
    asyncio.run(main())
