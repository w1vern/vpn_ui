

import uuid
from datetime import (
    UTC,
    datetime,
    timedelta,
)
from typing import Any

import jwt

from shared.database import (
    User,
)

from .config import (
    SECRET,
    Config,
)
from .schemas import (
    UserSchema,
)


def decode_jwt(token: str) -> dict[str, Any]:
    return jwt.decode(  # type: ignore
        token,
        key=SECRET,
        algorithms=[Config.algorithm])


def encode_jwt(payload: dict[str, Any]) -> str:
    return jwt.encode(  # type: ignore
        payload,
        key=SECRET)


class AccessToken:
    def __init__(self,
                 user: User | UserSchema | dict[str, Any],
                 created_date: datetime | str | None = None,
                 lifetime: timedelta | float | None = None
                 ) -> None:
        if created_date is None:
            self.created_date = datetime.now(UTC).replace(tzinfo=None)
        elif isinstance(created_date, str):
            self.created_date = datetime.fromisoformat(created_date)
        else:
            self.created_date = created_date
        if lifetime is None:
            self.lifetime = timedelta(seconds=Config.access_token_lifetime)
        elif isinstance(lifetime, (float, int)):
            self.lifetime = timedelta(seconds=lifetime)
        else:
            self.lifetime = lifetime
        if isinstance(user, dict):
            self.user = UserSchema(**user)
        elif isinstance(user, User):
            self.user = UserSchema.from_db(user)
        else:
            self.user = user

    @classmethod
    def from_token(cls, token: str) -> "AccessToken":
        return AccessToken(**decode_jwt(token))

    def to_token(self) -> str:
        return encode_jwt({
            "created_date": self.created_date.isoformat(),
            "lifetime": self.lifetime.total_seconds(),
            "user": self.user.model_dump(mode="json")
        })


class RefreshToken:
    def __init__(self,
                 user_id: uuid.UUID | str,
                 secret: str,
                 created_date: datetime | str | None = None,
                 lifetime: timedelta | float | None = None
                 ) -> None:
        self.secret = secret
        if created_date is None:
            self.created_date = datetime.now(UTC).replace(tzinfo=None)
        elif isinstance(created_date, str):
            self.created_date = datetime.fromisoformat(created_date)
        else:
            self.created_date = created_date
        if lifetime is None:
            self.lifetime = timedelta(seconds=Config.refresh_token_lifetime)
        elif isinstance(lifetime, (float, int)):
            self.lifetime = timedelta(seconds=lifetime)
        else:
            self.lifetime = lifetime
        if isinstance(user_id, str):
            self.user_id = uuid.UUID(user_id)
        else:
            self.user_id = user_id

    @classmethod
    def from_token(cls, token: str) -> "RefreshToken":
        return RefreshToken(**decode_jwt(token))

    def to_token(self) -> str:
        return encode_jwt({
            "created_date": self.created_date.isoformat(),
            "lifetime": self.lifetime.total_seconds(),
            "user_id": str(self.user_id),
            "secret": self.secret
        })
