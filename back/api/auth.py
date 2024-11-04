
from datetime import UTC, datetime
import random
from fastapi import Cookie, Depends, HTTPException, Response
from fastapi_controllers import Controller, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db_session
from database.redis import RedisType, get_redis_client
from database.repositories.user_repository import UserRepository
from back.schemes.tg_scheme import TgAuth, TgId
from back.config import Config
from back.broker import get_broker, send_message
from back.token import AccessToken, RefreshToken

def create_code() -> str:
	tmp_code = str(random.randrange(start=0, stop=1000000))
	return "0"*(6-len(tmp_code)) + tmp_code


class AuthController(Controller):
	prefix = "/auth"
	tags = ["auth"]

	def __init__(self, session: AsyncSession = Depends(get_db_session)):
		self.session = session

	@post("/refresh")
	async def refresh(self, response: Response, refresh_token: str = Cookie(None)):
		if refresh_token is None:
			raise HTTPException(
				status_code=401, detail="refresh token doesn\"t exist")
		refresh = RefreshToken.from_token(refresh_token)
		current_time = datetime.now(UTC)
		if refresh.created_date > current_time or refresh.created_date + refresh.lifetime < current_time:
			raise HTTPException(
				status_code=401, detail="refresh token expired")
		ur = UserRepository(self.session)
		user = await ur.get_by_id(refresh.user_id)
		if user is None:
			raise HTTPException(
				status_code=401, detail="incorrect refresh token")
		if user.secret != refresh.secret:
			raise HTTPException(
				status_code=401, detail="incorrect refresh token")
		access = AccessToken(user.id)
		response.set_cookie(key="access_token", value=access.to_token(
		), max_age=Config.access_token_lifetime, httponly=True)
		return {"message": "OK"}

	@post("/login")
	async def login(self, response: Response, tg_auth: TgAuth, redis=Depends(get_redis_client)):
		tg_code = redis.get(f"{RedisType.tg_code}:{tg_auth.tg_id}")
		if tg_code is None:
			raise HTTPException(status_code=401, detail="incorrect code")
		tg_code = tg_code.decode("utf-8")
		ur = UserRepository(self.session)
		user = await ur.get_by_telegram_id(tg_auth.tg_id)
		if user is None:
			raise HTTPException(status_code=401, detail="user not found")
		if tg_auth.tg_code != tg_code:
			raise HTTPException(status_code=401, detail="incorrect code")
		refresh = RefreshToken(user_id=user.id, secret=user.secret)
		access = AccessToken(user.id)
		response.set_cookie(key="refresh_token", value=refresh.to_token(
		), max_age=Config.refresh_token_lifetime, httponly=True)
		response.set_cookie(key="access_token", value=access.to_token(
		), max_age=Config.access_token_lifetime, httponly=True)
		return {"message": "OK"}

	@post("/logout")
	async def logout(self, response: Response):
		response.delete_cookie(key="refresh_token")
		response.delete_cookie(key="access_token")
		return {"message": "OK"}


	@post("/tg_code")
	async def tg_code(self, tg_id: TgId, broker=Depends(get_broker), redis=Depends(get_redis_client)):
		ur = UserRepository(self.session)
		user = await ur.get_by_telegram_id(tg_id.tg_id)
		if user is None:
			raise HTTPException(status_code=401, detail="user not found")
		tg_code = create_code()
		redis.set(f"{RedisType.tg_code}:{user.telegram_id}", tg_code, ex=Config.tg_code_lifetime)
		await send_message({"tg_id": tg_id.tg_id, "text": "your code to login: " + tg_code}, broker)
		return {"message": "OK"}