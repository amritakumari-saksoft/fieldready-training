import httpx
import pytest

from app.config import Settings
from app.services.llm_client import LLMClient


def make_settings(**overrides):
    values = {
        "llm_base_url": "https://example.com/v1",
        "llm_model": "primary-model",
        "llm_max_retries": 0,
    }
    values.update(overrides)
    return Settings(**values)


def test_successful_completion():
    def handler(request):
        assert request.url.path == "/v1/chat/completions"

        return httpx.Response(
            200,
            json={
                "model": "primary-model",
                "choices": [{"message": {"content": "Hello!"}}],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http:
        client = LLMClient(make_settings(), http)
        result = client.complete("Be helpful", "Say hello")

    assert result.content == "Hello!"
    assert result.model == "primary-model"
    assert result.usage.total_tokens == 15


def test_fallback_model():
    called_models = []

    def handler(request):
        import json

        model = json.loads(request.content)["model"]
        called_models.append(model)

        if model == "primary-model":
            return httpx.Response(503)

        return httpx.Response(
            200,
            json={
                "model": model,
                "choices": [{"message": {"content": "Fallback worked"}}],
            },
        )

    settings = make_settings(
        llm_fallback_models="backup-model",
    )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http:
        client = LLMClient(settings, http)
        result = client.complete("System", "User")

    assert result.content == "Fallback worked"
    assert called_models == ["primary-model", "backup-model"]


def test_no_model_configured():
    settings = make_settings(llm_model="")

    with httpx.Client() as http:
        client = LLMClient(settings, http)

        with pytest.raises(ValueError, match="No LLM model"):
            client.complete("System", "User")


def test_invalid_temperature():
    with httpx.Client() as http:
        client = LLMClient(make_settings(), http)

        with pytest.raises(ValueError, match="Temperature"):
            client.complete("System", "User", temperature=3.0)
