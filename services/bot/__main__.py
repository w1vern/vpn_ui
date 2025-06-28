
import asyncio

from .bot import bot, dp

from .rabbit import app


async def main():
    bot_task = asyncio.create_task(dp.start_polling(bot))
    app_task = asyncio.create_task(app.run())
    await asyncio.gather(
        bot_task,
        app_task
    )

if __name__ == "__main__":
    asyncio.run(main())
