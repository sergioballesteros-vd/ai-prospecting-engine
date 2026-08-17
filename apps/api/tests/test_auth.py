import pytest
from pydantic import ValidationError

from app.infrastructure.settings import Settings
from app.main import is_authorized_request


def test_api_token_auth_is_disabled_when_not_configured() -> None:
    assert is_authorized_request(None, None)


def test_api_token_auth_accepts_matching_bearer_token() -> None:
    assert is_authorized_request("secret-token", "Bearer secret-token")


def test_api_token_auth_rejects_missing_or_invalid_bearer_token() -> None:
    assert not is_authorized_request("secret-token", None)
    assert not is_authorized_request("secret-token", "Basic secret-token")
    assert not is_authorized_request("secret-token", "Bearer wrong-token")


def test_openai_provider_requires_api_auth_token() -> None:
    with pytest.raises(ValidationError):
        Settings(LLM_PROVIDER="openai", OPENAI_API_KEY="openai-key")


def test_openai_provider_accepts_api_auth_token() -> None:
    settings = Settings(
        LLM_PROVIDER="openai",
        OPENAI_API_KEY="openai-key",
        APP_API_TOKEN="app-token",
    )

    assert settings.llm_provider == "openai"
    assert settings.openai_model == "gpt-5.4-mini"
    assert settings.openai_reasoning_effort == "low"
