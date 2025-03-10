
import asyncio

from bot.consumer import app
from bot.main import bot


async def main():
    bot_task = asyncio.create_task(bot.infinity_polling())
    faststream_task = asyncio.create_task(app.start())
    await asyncio.gather(bot_task, faststream_task)


if __name__ == "__main__":
    asyncio.run(main())