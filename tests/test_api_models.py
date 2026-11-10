from datetime import date

import pytest
from pydantic import ValidationError

from app.models.api_models import Parcel, ParcelPage


def valid_parcel() -> dict:
    return {
        "id": 1,
        "name": "Birch 0001",
        "status": "active",
        "category": "charlie",
        "created": "2025-09-08",
    }


def test_valid_parcel() -> None:
    parcel = Parcel.model_validate(valid_parcel())

    assert parcel.id == 1
    assert parcel.name == "Birch 0001"
    assert parcel.created == date(2025, 9, 8)


def test_missing_status_is_rejected() -> None:
    data = valid_parcel()
    del data["status"]

    with pytest.raises(ValidationError):
        Parcel.model_validate(data)


def test_invalid_id_is_rejected() -> None:
    data = valid_parcel()
    data["id"] = -1

    with pytest.raises(ValidationError):
        Parcel.model_validate(data)


def test_invalid_date_is_rejected() -> None:
    data = valid_parcel()
    data["created"] = "invalid-date"

    with pytest.raises(ValidationError):
        Parcel.model_validate(data)


def test_valid_page() -> None:
    response = {
        "items": [valid_parcel()],
        "offset": 0,
        "limit": 5,
        "total": 237,
    }

    page = ParcelPage.model_validate(response)

    assert len(page.items) == 1
    assert page.total == 237


def test_missing_items_is_rejected() -> None:
    response = {
        "offset": 0,
        "limit": 5,
        "total": 237,
    }

    with pytest.raises(ValidationError):
        ParcelPage.model_validate(response)
