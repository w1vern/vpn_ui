from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db_session
from app.database.repositories.user_repository import UserRepository
from app.database.schemes.tg import TgAuth
from app.site.token import TgCode


router = APIRouter(prefix='/auth')


@router.post("/login")
async def login(tg_auth: TgAuth, tg_code: str = Cookie(None), session: AsyncSession = Depends(get_db_session)):
    tgCode = TgCode(jwt.decode(tg_code))
    ur = UserRepository(session)
    user = ur.get_by_telegram_id(tg_auth.tg_id)
    if user is None: 
        raise HTTPException(status_code=400, detail='user not found')
    if tg_auth.tg_code != tgCode.code:
        raise HTTPException(status_code=400, detail='incorrect password')
    
