from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_session
from .crud import create_user, get_user_by_email, get_all_users

app = FastAPI()

@app.post("/users/")
async def create_new_user(name: str, email: str, session: AsyncSession = Depends(get_session)):
    return await create_user(session, name, email)

@app.get("/users/")
async def list_users(session: AsyncSession = Depends(get_session)):
    return await get_all_users(session)

@app.get("/users/{email}")
async def get_user(email: str, session: AsyncSession = Depends(get_session)):
    return await get_user_by_email(session, email)
