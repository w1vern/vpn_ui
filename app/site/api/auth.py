
from datetime import UTC, datetime
import os
from dotenv import load_dotenv
from fastapi import Cookie, Depends, HTTPException, Response
from fastapi_controllers import Controller, get, post
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db_session
from app.database.models.user import User
from app.database.repositories.user_repository import UserRepository
from app.database.schemes.tg import TgAuth, TgId
from app.site.config import get_broker, send_message, SECRET
from app.site.token import AccessToken, RefreshToken, TgCode 


class AuthController(Controller):
    prefix='/auth'
    tags=['auth']
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    @post('/refresh')
    async def refresh(self, response: Response, refresh_token: str = Cookie(None)):
        if refresh_token is None:
            raise HTTPException(status_code=401, detail='refresh token not exist')
        refresh = RefreshToken.from_dict(jwt.decode(
            jwt=refresh_token, key=SECRET, algorithms='HS256'))
        current_time = datetime.now(UTC).replace(tzinfo=None)
        if refresh.created_date < current_time and refresh.created_date + refresh.lifetime > current_time:
            raise HTTPException(status_code=401, detail='refresh token expired')
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(refresh.user_id)
        if user is None:
            raise HTTPException(status_code=401, detail='incorrect refresh token')
        if user.secret != refresh.secret:
            raise HTTPException(status_code=401, detail='incorrect refresh token')
        access = AccessToken(user.id)
        response.set_cookie(key='access_token', value=jwt.encode(access.to_dict(), key=SECRET, algorithm='HS256'), max_age=60*10)

    @post("/login")
    async def login(self, response: Response, tg_auth: TgAuth, tg_code: str = Cookie(None)):
        tgCode = TgCode.from_dict(jwt.decode(tg_code, key=SECRET, algorithms='HS256'))
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(tg_auth.tg_id)
        if user is None: 
            raise HTTPException(status_code=401, detail='user not found')
        if tg_auth.tg_code != tgCode.code:
            raise HTTPException(status_code=401, detail='incorrect password')
        refresh = RefreshToken(user_id=user.id, secret=user.secret)
        access = AccessToken(user.id)
        response.set_cookie(key='refresh_token', value=jwt.encode(refresh.to_dict(), key=SECRET, algorithm='HS256'), max_age=30*24*3600)
        response.set_cookie(key='access_token', value=jwt.encode(access.to_dict(), key=SECRET, algorithm='HS256'), max_age=10*60)

    @post("/tg_code")
    async def get_tg_code(self, response: Response, tg_id: TgId, broker = Depends(get_broker)):
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(tg_id.tg_id)
        if user is None:
            raise HTTPException(status_code=401, detail='user not found')
        tgCode = TgCode()
        encoded = jwt.encode(tgCode.to_dict(), SECRET, algorithm="HS256")
        response.set_cookie(key='tg_code', value=encoded, httponly=True)
        await send_message({'tg_id': tg_id, 'text': tgCode.code}, broker)
        
        
    

            


    