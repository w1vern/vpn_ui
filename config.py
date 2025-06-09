
import os

from pydantic_settings import BaseSettings, DotEnvSettingsSource


class Settings(BaseSettings):
    db_user: str = "postgres"
    db_password: str = "1234"
    db_ip: str = "postgres"
    db_port: int = 5432
    db_name: str = "vpn_ui_db"
    redis_ip: str = "redis"
    redis_port: int = 6379
    rabbit_user: str = "guest"
    rabbit_password: str = "guest"
    rabbit_ip: str = "rabbitmq"
    rabbit_port: int = 5672
    bot_token: str = "YOUR_BOT_TOKEN"
    secret: str = "YOUR_SECRET"
    superuser_telegram_id: int = 0
    workers_count: int = 1
    compose_profiles: str = ""

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
