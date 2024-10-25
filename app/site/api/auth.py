
from datetime import UTC, datetime
from re import S
from fastapi import Cookie, Depends, HTTPException, Response
from fastapi_controllers import Controller, get, post
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db_session
from app.database.models.user import User
from app.database.repositories.user_repository import UserRepository
from app.database.schemes.tg import TgAuth, TgId
from app.site.config import config
from app.site.broker import get_broker, send_message
from app.site.config import SECRET
from app.site.token import AccessToken, RefreshToken, TgCode


class AuthController(Controller):
    prefix = '/auth'
    tags = ['auth']

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    @post('/refresh')
    async def refresh(self, response: Response, refresh_token: str = Cookie(None)):
        if refresh_token is None:
            raise HTTPException(
                status_code=401, detail='refresh token doesn\'t exist')
        refresh = RefreshToken.from_token(refresh_token)
        current_time = datetime.now(UTC)
        if refresh.created_date > current_time or refresh.created_date + refresh.lifetime < current_time:
            raise HTTPException(
                status_code=401, detail='refresh token expired')
        ur = UserRepository(self.session)
        user = await ur.get_by_id(refresh.user_id)
        if user is None:
            raise HTTPException(
                status_code=401, detail='incorrect refresh token')
        if user.secret != refresh.secret:
            raise HTTPException(
                status_code=401, detail='incorrect refresh token')
        access = AccessToken(user.id)
        response.set_cookie(key='access_token', value=access.to_token(
        ), max_age=config['access_token_lifetime'])
        print(refresh.created_date + refresh.lifetime)
        print(access.created_date + access.lifetime)

    @post("/login")
    async def login(self, response: Response, tg_auth: TgAuth, tg_code: str = Cookie(None)):
        tg_code_class = TgCode.from_token(tg_code)
        current_time = datetime.now(UTC)
        if tg_code_class.created_date > current_time or tg_code_class.created_date + tg_code_class.lifetime < current_time:
            raise HTTPException(status_code=401, detail='telegram code expired')
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(tg_auth.tg_id)
        if user is None:
            raise HTTPException(status_code=401, detail='user not found')
        if tg_code_class.user_id != user.id:
            raise HTTPException(status_code=401, detail='wtf you doing?!?')
        if tg_auth.tg_code != tg_code_class.code:
            raise HTTPException(status_code=401, detail='incorrect code')
        refresh = RefreshToken(user_id=user.id, secret=user.secret)
        access = AccessToken(user.id)
        response.set_cookie(key='refresh_token', value=refresh.to_token(
        ), max_age=config['refresh_token_lifetime'])
        response.set_cookie(key='access_token', value=access.to_token(
        ), max_age=config['access_token_lifetime'])

    @post("/tg_code")
    async def tg_code(self, response: Response, tg_id: TgId, broker=Depends(get_broker)):
        ur = UserRepository(self.session)
        user = await ur.get_by_telegram_id(tg_id.tg_id)
        if user is None:
            raise HTTPException(status_code=401, detail='user not found')
        tg_code = TgCode(user.id)
        response.set_cookie(
            key='tg_code', value=tg_code.to_token(), max_age=config['tg_code_lifetime'])
        await send_message({'tg_id': tg_id.tg_id, 'text': 'your code to login: ' + tg_code.code}, broker)
