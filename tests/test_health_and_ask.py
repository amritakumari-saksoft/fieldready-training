from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_alive_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_no_problems_returns_ready():
    with patch(
        "app.services.readiness.check_dependencies",
        return_value=[],
    ):
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_request_id_is_returned_and_reused():
    response = client.get("/health")

    assert "X-Request-ID" in response.headers


def test_ask_without_sources_says_i_dont_know():
    with patch(
        "app.services.answering.retrieve",
        return_value=[],
    ):
        response = client.post(
            "/ask",
            json={"question": "What is the loan limit?"},
        )

    assert response.status_code == 200

    data = response.json()

    assert "don't know" in data["answer"].lower()
    assert data["citations"] == []


def test_ask_empty_question_is_rejected_with_422():
    response = client.post(
        "/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_ask_very_long_question_is_rejected_with_422():
    response = client.post(
        "/ask",
        json={"question": "a" * 10001},
    )

    assert response.status_code == 422
