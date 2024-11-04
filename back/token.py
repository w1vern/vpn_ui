

from datetime import UTC, timedelta, datetime, timezone
import random
import uuid

import jwt

from back.config import SECRET, Config


class AccessToken:
    def __init__(self, user_id: uuid.UUID | str, created_date: datetime | str = datetime.now(UTC), lifetime: timedelta | float = timedelta(seconds=Config.access_token_lifetime)) -> None:
        if type(created_date) == str:
            self.created_date = datetime.fromisoformat(created_date)
        else:
            self.created_date = created_date
        if type(lifetime) == float:
            self.lifetime = timedelta(seconds=lifetime)
        else:
            self.lifetime = lifetime
        if type(user_id) == str:
            self.user_id = uuid.UUID(user_id)
        else:
            self.user_id = user_id

    @classmethod
    def from_token(cls, token: str) -> "AccessToken":
        return AccessToken(**jwt.decode(jwt=token, key=SECRET, algorithms=Config.algorithm))

    def to_token(self) -> str:
        return jwt.encode(payload={
            "created_date": self.created_date.isoformat(),
            "lifetime": self.lifetime.total_seconds(),
            "user_id": str(self.user_id)
        }, key=SECRET)


class RefreshToken:
    def __init__(self, user_id: uuid.UUID | str, secret: str, created_date: datetime | str = datetime.now(UTC), lifetime: timedelta | float = timedelta(seconds=Config.refresh_token_lifetime)) -> None:
        self.secret = secret
        if type(created_date) == str:
            self.created_date = datetime.fromisoformat(created_date)
        else:
            self.created_date = created_date
        if type(lifetime) == float:
            self.lifetime = timedelta(seconds=lifetime)
        else:
            self.lifetime = lifetime
        if type(user_id) == str:
            self.user_id = uuid.UUID(user_id)
        else:
            self.user_id = user_id

    @classmethod
    def from_token(cls, token: str) -> "RefreshToken":
        return RefreshToken(**jwt.decode(jwt=token, key=SECRET, algorithms=Config.algorithm))

    def to_token(self) -> str:
        return jwt.encode(payload={
            "created_date": self.created_date.isoformat(),
            "lifetime": self.lifetime.total_seconds(),
            "user_id": str(self.user_id),
            "secret": self.secret
        }, key=SECRET)
