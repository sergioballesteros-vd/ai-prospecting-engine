from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./prospecting.db", alias="DATABASE_URL")
    app_api_token: str | None = Field(default=None, alias="APP_API_TOKEN")
    llm_provider: str = Field(default="stub", alias="LLM_PROVIDER")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5.4-mini", alias="OPENAI_MODEL")
    openai_reasoning_effort: Literal["none", "low", "medium", "high", "xhigh"] = Field(
        default="low", alias="OPENAI_REASONING_EFFORT"
    )
    discovery_provider: str = Field(default="csv", alias="DISCOVERY_PROVIDER")
    discovery_csv_path: str | None = Field(default=None, alias="DISCOVERY_CSV_PATH")
    research_max_pages: int = Field(default=12, ge=1, le=50, alias="RESEARCH_MAX_PAGES")
    research_max_content_bytes: int = Field(
        default=180_000, ge=10_000, le=2_000_000, alias="RESEARCH_MAX_CONTENT_BYTES"
    )
    research_timeout_seconds: float = Field(
        default=10.0, ge=1.0, le=60.0, alias="RESEARCH_TIMEOUT_SECONDS"
    )
    research_retries: int = Field(default=1, ge=0, le=5, alias="RESEARCH_RETRIES")
    research_rate_limit_seconds: float = Field(
        default=0.25, ge=0.0, le=5.0, alias="RESEARCH_RATE_LIMIT_SECONDS"
    )
    overpass_endpoint: str = Field(
        default="https://overpass-api.de/api/interpreter", alias="OVERPASS_ENDPOINT"
    )
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000", alias="CORS_ORIGINS"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @field_validator("app_api_token", "openai_api_key", "discovery_csv_path", mode="before")
    @classmethod
    def blank_string_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @model_validator(mode="after")
    def require_auth_for_openai(self) -> "Settings":
        if self.llm_provider == "openai" and not self.app_api_token:
            raise ValueError("APP_API_TOKEN is required when LLM_PROVIDER=openai")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
