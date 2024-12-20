

from datetime import UTC, datetime

from database.database import session_manager
from database.repositories.server_repository import ServerRepository


async def check_servers() -> None:
    async with session_manager.session() as session:
        sr = ServerRepository(session)
        servers = await sr.get_all()
        current_date = datetime.now(UTC).replace(tzinfo=None)
        for server in servers:
            if server.is_available and server.closing_date < current_date:
                await sr.set_is_available(server, False)