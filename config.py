
import os

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings, DotEnvSettingsSource, SettingsConfigDict)


class DBSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    user: str = "postgres"
    password: str = "1234"
    ip: str = "postgres"
    port: int = 5432
    name: str = "vpn_ui_db"


class RedisSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    ip: str = "redis"
    port: int = 6379


class RabbitSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    user: str = "guest"
    password: str = "guest"
    ip: str = "rabbitmq"
    port: int = 5672


class BotSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    token: str = "YOUR_BOT_TOKEN"
    superuser_id: int = 0


class BackendSettings(BaseModel):
    model_config = SettingsConfigDict(
        populate_by_name=True)

    secret: str = "YOUR_SECRET"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        extra="ignore"
    )

    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()
    rabbit: RabbitSettings = RabbitSettings()
    bot: BotSettings = BotSettings()
    backend: BackendSettings = BackendSettings()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        target_env = os.getenv("TARGET", "dev.") + "env"
        return (
            init_settings,
            DotEnvSettingsSource(settings_cls, env_file=target_env),
            file_secret_settings
        )


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump_json(indent=2))
