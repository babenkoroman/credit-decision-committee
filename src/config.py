from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Credit Decision Committee"
    debug: bool = False
    api_prefix: str = "/api/v1"

    database_url: str

    deepseek_api_key: str 

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
