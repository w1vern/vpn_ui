
import os
from enum import Enum

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class BootLevel(str, Enum):
    DEBUG = "DEBUG"
    TEST = "TEST"
    RELEASE = "RELEASE"


class DBSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    user: str = ""
    password: str = ""
    ip: str = ""
    port: int = 0
    name: str = ""


class RedisSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    ip: str = ""
    port: int = 0
    login: str | None = None
    password: str | None = None
    backend: int = 0
    bot: int = 1


class RabbitSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    user: str = ""
    password: str = ""
    ip: str = ""
    port: int = 0


class BotSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True,
    )

    token: str = ""
    superuser: int = 0


class BackendSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    secret: str = ""
    workers: int = 0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", "dev.env"),
        env_nested_delimiter="_",
        extra="ignore"
    )

    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    rabbit: RabbitSettings = RabbitSettings()
    bot: BotSettings = BotSettings()
    backend: BackendSettings = BackendSettings()
    boot_level: BootLevel = BootLevel.DEBUG


env_config = Settings()

if env_config.redis.login == "":
    env_config.redis.login = None

if env_config.redis.password == "":
    env_config.redis.password = None

if env_config.bot.superuser == 0:
    raise ValueError("env parameters not set")

if __name__ == "__main__":
    print(env_config.model_dump_json(indent=2))
