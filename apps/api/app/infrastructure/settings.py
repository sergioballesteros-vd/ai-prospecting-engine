from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./prospecting.db", alias="DATABASE_URL")
    llm_provider: str = Field(default="stub", alias="LLM_PROVIDER")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    discovery_provider: str = Field(default="csv", alias="DISCOVERY_PROVIDER")
    discovery_csv_path: str | None = Field(default=None, alias="DISCOVERY_CSV_PATH")
    overpass_endpoint: str = Field(
        default="https://overpass-api.de/api/interpreter", alias="OVERPASS_ENDPOINT"
    )
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000", alias="CORS_ORIGINS"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
