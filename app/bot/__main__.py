
from app.bot.main import bot
import app.bot.handlers
import asyncio

if __name__ == "__main__":
    asyncio.run(bot.infinity_polling())


