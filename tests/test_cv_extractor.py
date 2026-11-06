import pytest

from app.models.cv_models import CVData
from app.services.cv_extractor import CVExtractor
from app.services.llm_client import LLMResult, TokenUsage


class FakeLLMClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = 0

    def complete(self, system_prompt, user_prompt, temperature=0.0):
        self.calls += 1
        return LLMResult(
            content=next(self.responses),
            model="test-model",
            usage=TokenUsage(),
        )


def test_valid_cv_extraction():
    fake_client = FakeLLMClient(
        [
            '{"full_name": "Priya Sharma", '
            '"email": "priya@example.com", '
            '"phone": "9876543210", '
            '"skills": ["Python", "SQL"], '
            '"education": ["B.Tech"], '
            '"experience_years": 2}'
        ]
    )

    extractor = CVExtractor(fake_client)
    result = extractor.extract("Priya Sharma, Python developer")

    assert isinstance(result, CVData)
    assert result.full_name == "Priya Sharma"
    assert result.skills == ["Python", "SQL"]
    assert result.experience_years == 2
    assert fake_client.calls == 1


def test_invalid_json_repair():
    fake_client = FakeLLMClient(
        [
            "This is not JSON",
            '{"full_name": "Rahul", "skills": ["Python"]}',
        ]
    )

    extractor = CVExtractor(fake_client)
    result = extractor.extract("Rahul knows Python")

    assert result.full_name == "Rahul"
    assert fake_client.calls == 2


def test_repair_failure():
    fake_client = FakeLLMClient(
        [
            "Invalid JSON",
            "Still invalid JSON",
        ]
    )

    extractor = CVExtractor(fake_client)

    with pytest.raises(ValueError, match="repair retry"):
        extractor.extract("Sample CV")

    assert fake_client.calls == 2


def test_empty_cv():
    fake_client = FakeLLMClient([])

    extractor = CVExtractor(fake_client)

    with pytest.raises(ValueError, match="empty"):
        extractor.extract("   ")

    assert fake_client.calls == 0
