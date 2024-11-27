import asyncio
import secrets
from database.enums.role import Role
from database.models.server import Server
from datetime import datetime, UTC, timedelta
from database.database import session_manager

from database.models.user import User
from database.repositories.server_repository import ServerRepository
from database.repositories.user_repository import UserRepository

server = Server(ip="3xui.demogram.ru", panel_path="", country_code="ru", display_name="1", login="admin", password="admin",
                is_available=True, created_date=datetime.now(UTC).replace(tzinfo=None), closing_date=(datetime.now(UTC) + timedelta(days=30)).replace(tzinfo=None), vless_id=0, vless_reality_id=0, vmess_id=0)


user = User(telegram_id=101, telegram_username="aboba1", balance=0, role=Role.admin, active=True,
            auto_pay=False, created_date=datetime.now(UTC).replace(tzinfo=None), secret=secrets.token_urlsafe())

async def main():
    async with session_manager.session() as session:
        session.add(server)
        session.add(user)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
