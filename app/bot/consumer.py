from app.bot.main import app, broker
from app.database.repositories.user_repository import User
from app.database.database import get_db

import json

session = get_db()

@broker.subscriber("back/start")
async def start(msg: str):
    