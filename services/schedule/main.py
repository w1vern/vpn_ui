
import asyncio
from datetime import timedelta

import aioschedule as schedule

from schedule.server import check_servers
from schedule.user import check_users


async def main():
    schedule.every(1).hours.do(check_users)
    schedule.every(1).hours.do(check_servers)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(timedelta(hours=1).total_seconds())