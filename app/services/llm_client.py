"""OpenAI-compatible LLM client with retries and fallback models."""

import logging
import time

import httpx
from pydantic import BaseModel, Field

from app.config import Settings

logger = logging.getLogger(__name__)


class TokenUsage(BaseModel):
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)


class LLMResult(BaseModel):
    content: str
    model: str
    usage: TokenUsage


class LLMClient:
    """Call OpenAI-compatible chat completion endpoints."""

    def __init__(
        self,
        settings: Settings,
        http_client: httpx.Client,
    ) -> None:
        if settings.llm_timeout_seconds <= 0:
            raise ValueError("LLM timeout must be positive")
        if settings.llm_max_retries < 0:
            raise ValueError("LLM retries cannot be negative")

        self.settings = settings
        self.http_client = http_client

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> LLMResult:
        """Generate a response, trying fallback models if necessary."""

        models = [
            self.settings.llm_model,
            *self.settings.llm_fallback_models.split(","),
        ]
        models = list(dict.fromkeys(m.strip() for m in models if m.strip()))

        if not models:
            raise ValueError("No LLM model configured")

        if not 0 <= temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")

        headers = {"Content-Type": "application/json"}
        api_key = self.settings.llm_api_key.get_secret_value()

        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        for model in models:
            for attempt in range(self.settings.llm_max_retries + 1):
                try:
                    response = self.http_client.post(
                        f"{self.settings.llm_base_url.rstrip('/')}/chat/completions",
                        headers=headers,
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt},
                            ],
                            "temperature": temperature,
                        },
                        timeout=self.settings.llm_timeout_seconds,
                    )

                    response.raise_for_status()
                    data = response.json()

                    return LLMResult(
                        content=data["choices"][0]["message"]["content"],
                        model=data.get("model", model),
                        usage=TokenUsage.model_validate(data.get("usage") or {}),
                    )

                except (
                    httpx.TimeoutException,
                    httpx.NetworkError,
                    httpx.HTTPStatusError,
                ) as exc:
                    retryable = not isinstance(
                        exc, httpx.HTTPStatusError
                    ) or exc.response.status_code in (408, 429, 500, 502, 503, 504)

                    logger.warning(
                        "LLM request failed for model %s: %s",
                        model,
                        type(exc).__name__,
                    )

                    if not retryable or attempt >= self.settings.llm_max_retries:
                        break

                    time.sleep(min(2**attempt, 8))

        raise RuntimeError("All configured LLM models failed")
