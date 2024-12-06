from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os

class Settings(BaseSettings):
    # DB_HOST: SecretStr
    # DB_PORT: int
    # DB_USER: SecretStr
    # DB_PASS: SecretStr
    # DB_NAME: SecretStr
    BOT_TOKEN: SecretStr
    DB_URL: SecretStr
    model_config = SettingsConfigDict(
        env_file = ".env"
    )

    # class Config:
    #     env_file = ".env"

settings = Settings()