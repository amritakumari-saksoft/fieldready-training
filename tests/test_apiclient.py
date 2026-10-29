import httpx
import pytest

from app.services.apiclient import APIClient


def parcel_record(parcel_id: int) -> dict:
    return {
        "id": parcel_id,
        "name": f"Parcel {parcel_id}",
        "status": "active",
        "category": "alpha",
        "created": "2025-09-08",
    }


def test_successful_request() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/parcels"
        assert request.extensions["timeout"]["read"] > 0

        return httpx.Response(
            200,
            json={
                "items": [parcel_record(1)],
                "offset": 0,
                "limit": 5,
                "total": 1,
            },
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
        )

        parcels = list(client.iter_parcels(page_size=5))

    assert len(parcels) == 1
    assert parcels[0].id == 1


def test_retries_after_server_error() -> None:
    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        if attempts == 1:
            return httpx.Response(500)

        return httpx.Response(
            200,
            json={
                "items": [parcel_record(1)],
                "offset": 0,
                "limit": 5,
                "total": 1,
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
            backoff_factor=0,
        )

        parcels = list(client.iter_parcels(page_size=5))

    assert attempts == 2
    assert len(parcels) == 1


def test_invalid_record_is_rejected() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        invalid_record = parcel_record(1)
        del invalid_record["status"]

        return httpx.Response(
            200,
            json={
                "items": [invalid_record],
                "offset": 0,
                "limit": 5,
                "total": 1,
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
        )

        with pytest.raises(ValueError, match="status"):
            list(client.iter_parcels(page_size=5))


def test_retries_after_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = 0
    delays: list[float] = []
    monkeypatch.setattr("app.services.apiclient.time.sleep", delays.append)

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(429, headers={"Retry-After": "2"})
        return httpx.Response(
            200,
            json={
                "items": [parcel_record(1)],
                "offset": 0,
                "limit": 5,
                "total": 1,
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
        )
        parcels = list(client.iter_parcels(page_size=5))

    assert attempts == 2
    assert delays == [2.0]
    assert len(parcels) == 1


def test_timeout_is_raised() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Simulated timeout", request=request)

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
            timeout=0.5,
        )
        with pytest.raises(httpx.ReadTimeout):
            list(client.iter_parcels(page_size=5))


def test_duplicate_parcels_are_removed() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        offset = int(request.url.params["offset"])

        if offset == 0:
            items = [parcel_record(1), parcel_record(2)]
        elif offset == 2:
            items = [parcel_record(2), parcel_record(3)]
        else:
            items = []

        return httpx.Response(
            200,
            json={
                "items": items,
                "offset": offset,
                "limit": 2,
                "total": 4,
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
        )
        parcels = list(client.iter_parcels(page_size=2))

    assert [parcel.id for parcel in parcels] == [1, 2, 3]


def test_retry_exhaustion(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = 0
    monkeypatch.setattr(
        "app.services.apiclient.time.sleep",
        lambda delay: None,
    )

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(503)

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
            max_retries=2,
        )
        with pytest.raises(httpx.HTTPStatusError):
            list(client.iter_parcels(page_size=5))

    assert attempts == 3


def test_invalid_json_is_rejected() -> None:
    from json import JSONDecodeError

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            content=b"not valid JSON",
            headers={"content-type": "application/json"},
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
        )
        with pytest.raises(JSONDecodeError):
            list(client.iter_parcels(page_size=5))


def test_exponential_backoff_with_jitter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    delays: list[float] = []

    monkeypatch.setattr(
        "app.services.apiclient.secrets.randbelow",
        lambda upper: 500,
    )
    monkeypatch.setattr(
        "app.services.apiclient.time.sleep",
        delays.append,
    )

    attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        if attempts <= 2:
            return httpx.Response(503)

        return httpx.Response(
            200,
            json={
                "items": [parcel_record(1)],
                "offset": 0,
                "limit": 5,
                "total": 1,
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = APIClient(
            base_url="http://example.test",
            http_client=http_client,
            backoff_factor=1.0,
        )

        parcels = list(client.iter_parcels(page_size=5))

    assert attempts == 3
    assert delays == [1.5, 3.0]
    assert len(parcels) == 1
