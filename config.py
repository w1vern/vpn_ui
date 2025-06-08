import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{os.getenv('TARGET', 'dev')}.env")
    
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

settings = Settings()
