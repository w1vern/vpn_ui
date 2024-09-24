from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User

async def create_user(session: AsyncSession, name: str, email: str):
    new_user = User(name=name, email=email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()
