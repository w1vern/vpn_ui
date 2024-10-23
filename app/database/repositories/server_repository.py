from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID, select
from app.database.models import *
from typing import Optional
from datetime import datetime, UTC


class ServerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session