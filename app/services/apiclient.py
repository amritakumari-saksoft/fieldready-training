import logging
import secrets
import time
from collections.abc import Iterator
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import httpx

from app.models.api_models import Parcel, ParcelPage

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client for the Training Mock Parcels API."""

    def __init__(
        self,
        base_url: str,
        http_client: httpx.Client,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if backoff_factor < 0:
            raise ValueError("backoff_factor cannot be negative")

        self.base_url = base_url.rstrip("/")
        self.http_client = http_client
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _retry_delay(self, response: httpx.Response, attempt: int) -> float:
        """Calculate retry delay using Retry-After or exponential backoff."""
        retry_after = response.headers.get("Retry-After")

        if retry_after:
            try:
                return max(0.0, float(retry_after))
            except ValueError:
                try:
                    retry_date = parsedate_to_datetime(retry_after)

                    if retry_date.tzinfo is None:
                        retry_date = retry_date.replace(tzinfo=UTC)

                    return max(
                        0.0,
                        (retry_date - datetime.now(UTC)).total_seconds(),
                    )
                except TypeError, ValueError, OverflowError:
                    logger.warning("Invalid Retry-After header")

        delay = self.backoff_factor * (2**attempt)
        jitter = secrets.randbelow(1001) / 1000 * delay

        return delay + jitter

    def _get(self, path: str, params: dict[str, int]) -> httpx.Response:
        """Send an HTTP GET request with timeout and retry handling."""
        url = f"{self.base_url}{path}"

        for attempt in range(self.max_retries + 1):
            try:
                response = self.http_client.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                )
            except httpx.TimeoutException:
                logger.warning("API request timed out")
                raise

            if (
                response.status_code == 429 or 500 <= response.status_code <= 599
            ) and attempt < self.max_retries:
                delay = self._retry_delay(response, attempt)

                logger.warning(
                    "API returned status %s; retrying",
                    response.status_code,
                )

                time.sleep(delay)
                continue

            response.raise_for_status()
            return response

        raise RuntimeError("Retry attempts exhausted")

    def iter_parcels(self, page_size: int = 20) -> Iterator[Parcel]:
        """Yield validated parcels without duplicate IDs."""
        if page_size <= 0:
            raise ValueError("page_size must be positive")

        offset = 0
        seen_ids: set[int] = set()

        while True:
            response = self._get(
                "/v1/parcels",
                {"offset": offset, "limit": page_size},
            )

            page = ParcelPage.model_validate(response.json())

            if not page.items:
                break

            for parcel in page.items:
                if parcel.id not in seen_ids:
                    seen_ids.add(parcel.id)
                    yield parcel

            offset += page_size

            if offset >= page.total:
                break
