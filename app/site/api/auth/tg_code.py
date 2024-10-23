import json
from aiormq import Channel
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db_session
from app.database.repositories.user_repository import UserRepository
from app.database.schemes.tg import TgId
from app.site.main import SECRET, send_message
from app.site.token import TgCode
import jwt


router = APIRouter(prefix='/auth')

@router.post("/tg_code")
async def get_tg_code(response: Response, tg_id: TgId, session: AsyncSession = Depends(get_db_session)):
    ur = UserRepository(session)
    user = await ur.get_by_telegram_id(tg_id)
    if user is None:
        raise HTTPException(status_code=400, detail='user not found')
    tgCode = TgCode()
    encoded = jwt.encode(tgCode.to_dict(), SECRET, algorithm="HS256")
    response.set_cookie(key='tg_code', value=encoded, httponly=True)
    send_message({'tg_id': tg_id, 'text': tgCode.code})
    
    
    