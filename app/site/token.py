

from datetime import timedelta, datetime, timezone
import random
import secrets
import uuid

import jwt

from app.site.config import SECRET



class AccessToken:
    def __init__(self, user_id: uuid.UUID, created_date: datetime = datetime.now(tz=timezone.utc), lifetime: timedelta = timedelta(minutes=10)) -> None:
        self.nbf = created_date
        self.exp = lifetime + created_date
        self.user_id = user_id

    @classmethod
    def from_dict(cls, dict: dict) -> 'AccessToken':
        return AccessToken()
    
    @classmethod
    def from_token(cls, token: str) -> 'AccessToken':
        return AccessToken.from_dict(jwt.decode(jwt=token, key=SECRET))

    def to_token(self) -> dict:
        return jwt.encode(payload={
            'nbf': self.nbf,
            'exp': self.exp,
            'user_id': str(self.user_id)
        }, key=SECRET)

class RefreshToken:
    def __init__(self, user_id: uuid.UUID, secret: str = secrets.token_urlsafe(), created_date: datetime = datetime.now(tz=timezone.utc), lifetime: timedelta = timedelta(minutes=10)) -> None:
        self.nbf = created_date
        self.exp = lifetime + created_date
        self.user_id = user_id
        self.secret = secret

    @classmethod
    def from_dict(cls, dict: dict) -> 'RefreshToken':
        return RefreshToken()
    
    @classmethod
    def from_token(cls, token: str) -> 'RefreshToken':
        return RefreshToken.from_dict(jwt.decode(jwt=token, key=SECRET))

    def to_token(self) -> dict:
        return jwt.encode(payload={
            'nbf': str(self.nbf),
            'exp': str(self.exp),
            'user_id': str(self.user_id)
            'secret': 
        }, key=SECRET)

class RefreshToken:
    def __init__(self, user_id: uuid.UUID, secret: str, created_date: datetime = datetime.now().replace(tzinfo=None), lifetime: timedelta = timedelta(days=30)) -> None:
        self.created_date = created_date
        self.lifetime = lifetime
        self.user_id = user_id
        self.secret = secret

    @classmethod
    def from_dict(cls, dict: dict) -> 'RefreshToken':
        return RefreshToken(user_id=dict['user_id'], created_date=datetime.fro(dict['created_date']), lifetime=timedelta(dict['lifetime']), secret=dict['secret'])

    def to_dict(self) -> dict:
        return {
            'created_date': self.created_date.isoformat(),
            'lifetime': self.lifetime.,
            'user_id': str(self.user_id),
            'secret': self.secret
        }


class TgCode:
    def __init__(self, code: str = None, created_date: datetime = datetime.now().replace(tzinfo=None), lifetime: timedelta = timedelta(minutes=2)) -> None:
        self.created_date = created_date
        self.lifetime = lifetime
        if code is None:
            tmp_code = str(random.randrange(start=0, stop=1000000))
            self.code = '0'*(6-len(tmp_code)) + tmp_code
        else:
            self.code = code

    @classmethod
    def from_dict(cls, dict: dict) -> 'TgCode':
        return TgCode(code=dict['code'], created_date=dict['created_date'], lifetime=dict['lifetime'])

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'created_date': self.created_date.isoformat(),
            'lifetime': self.lifetime.total_seconds()
        }
