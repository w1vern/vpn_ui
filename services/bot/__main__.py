
import asyncio

from .bot import bot, dp
from .rabbit import app
from .handlers import router
from .lifecycle import register_lifecycle


async def main():
    register_lifecycle(dp, bot)
    dp.include_router(router)
    bot_task = asyncio.create_task(dp.start_polling(bot))
    # broker_task = asyncio.create_task(app.run())
    await asyncio.gather(
        bot_task,
        # broker_task
    )

if __name__ == "__main__":
    asyncio.run(main())
