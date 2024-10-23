

from datetime import timedelta, datetime
import random
import uuid


class AccessToken:
    def __init__(self, user_id: uuid.UUID, created_date: datetime = datetime.now().replace(tzinfo=None), lifetime: timedelta = timedelta(minutes=10)) -> None:
        self.created_date = created_date
        self.lifetime = lifetime
        self.user_id = user_id

    


class RefreshToken:
    def __init__(self, user_id: uuid.UUID, secret: str, created_date: datetime = datetime.now().replace(tzinfo=None), lifetime: timedelta = timedelta(days=30)) -> None:
        self.created_date = created_date
        self.lifetime = lifetime
        self.user_id = user_id
        self.secret = secret


class TgCode:
    def __init__(self, code: str = None, created_date: datetime = datetime.now().replace(tzinfo=None), lifetime: timedelta = timedelta(minutes=2)) -> None:
        self.created_date = created_date
        self.lifetime = lifetime
        if code is None:
            tmp_code = str(random.randrange(stop=1000000))
            self.code = '0'*len(tmp_code) + tmp_code
        else:
            self.code = code

    def __init__(self, dict: dict) -> None:
        self.created_date = datetime.fromisoformat(dict['created_date'])
        self.lifetime = timedelta(seconds=dict['lifetime'])
        self.code = dict['code']

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'created_date': self.created_date.isoformat(),
            'lifetime': self.lifetime.total_seconds()
        }
