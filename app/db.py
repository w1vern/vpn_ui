from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# URL подключения к базе данных
load_dotenv()
DATABASE_URL = os.getenv("db_tmp_url")

print(DATABASE_URL)

# Создание асинхронного движка базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия для работы с БД
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()

# Асинхронная функция для получения сессии
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
