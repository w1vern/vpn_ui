
import asyncio

from .bot import bot, dp
from .handlers import router
from .lifecycle import register_lifecycle
from .rabbit import app


async def main():
    register_lifecycle(dp, bot)
    dp.include_router(router)
    bot_task = asyncio.create_task(dp.start_polling(bot))
    broker_task = asyncio.create_task(app.start())
    try:
        await asyncio.gather(
            bot_task,
            broker_task
        )
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
