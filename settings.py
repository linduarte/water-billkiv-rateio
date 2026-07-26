"""Application configuration loaded via Pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    supabase_url: str
    supabase_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings_kwargs: dict[str, str] = {}
settings = Settings(**settings_kwargs)
