from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, EmailStr, Field


class Settings(BaseSettings):
    app_name: str = "Card Science Insight"
    environment: str = Field("development", description="App environment name")
    secret_key: str = Field("CHANGE_ME_SUPER_SECRET", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = Field(
        default="sqlite+aiosqlite:///./card_science.db",
        env="DATABASE_URL",
    )

    mail_sender: EmailStr = Field("no-reply@cardsci.app", env="MAIL_SENDER")
    mail_from_name: str = "Card Science Insight"
    mail_smtp_host: str = Field("smtp.gmail.com", env="MAIL_SMTP_HOST")
    mail_smtp_port: int = Field(587, env="MAIL_SMTP_PORT")
    mail_username: Optional[str] = Field(None, env="MAIL_USERNAME")
    mail_password: Optional[str] = Field(None, env="MAIL_PASSWORD")
    mail_use_tls: bool = Field(True, env="MAIL_USE_TLS")

    railway_port: int = Field(8000, env="PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
