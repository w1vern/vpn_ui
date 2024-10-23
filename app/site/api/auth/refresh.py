from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db_session


router = APIRouter(prefix='/auth')

@router.get("/refresh")
def m1():
    pass