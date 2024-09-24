import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .db import DATABASE_URL

def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
