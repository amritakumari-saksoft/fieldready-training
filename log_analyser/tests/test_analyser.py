# ruff: noqa: S101
from pathlib import Path

import pytest
from analyser import analyse_log
from exceptions import LogFileError


def test_info_count(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-10-28 10:00:00 INFO Application started\n",
        encoding="utf-8",
    )

    result = analyse_log(str(log_file))

    assert result["counts_by_level"] == {"INFO": 1}


def test_error_count(tmp_path: Path) -> None:
    log_file = tmp_path / "errors.log"

    log_file.write_text(
        "2026-10-28 10:00:00 ERROR Database failed\n2026-10-28 10:01:00 ERROR Connection lost\n",
        encoding="utf-8",
    )

    result = analyse_log(str(log_file))

    assert result["counts_by_level"] == {"ERROR": 2}


def test_warning_count(tmp_path: Path) -> None:
    log_file = tmp_path / "warnings.log"

    log_file.write_text(
        "2026-10-28 10:00:00 WARNING Slow response\n"
        "2026-10-28 10:01:00 WARNING High memory usage\n",
        encoding="utf-8",
    )

    result = analyse_log(str(log_file))

    assert result["counts_by_level"] == {"WARNING": 2}


def test_invalid_log_lines(tmp_path: Path) -> None:
    log_file = tmp_path / "invalid.log"

    log_file.write_text(
        "2026-10-28 10:00:00 INFO Application started\n"
        "INVALID LOG LINE\n"
        "2026-10-28 10:01:00 ERROR Database failed\n",
        encoding="utf-8",
    )

    result = analyse_log(str(log_file))

    assert result["bad_lines"] == 1
    assert result["counts_by_level"] == {
        "INFO": 1,
        "ERROR": 1,
    }


def test_top_errors(tmp_path: Path) -> None:
    log_file = tmp_path / "errors.log"

    log_file.write_text(
        "2026-10-28 10:00:00 ERROR Database failed\n"
        "2026-10-28 10:01:00 ERROR Connection lost\n"
        "2026-10-28 10:02:00 ERROR Database failed\n",
        encoding="utf-8",
    )

    result = analyse_log(str(log_file))

    assert result["top_errors"] == [
        {"message": "Database failed", "count": 2},
        {"message": "Connection lost", "count": 1},
    ]


def test_time_range(tmp_path: Path) -> None:
    log_file = tmp_path / "time.log"

    log_file.write_text(
        "2026-10-28 10:05:00 INFO Last event\n"
        "2026-10-28 10:00:00 INFO First event\n"
        "2026-10-28 10:03:00 ERROR Database failed\n",
        encoding="utf-8",
    )

    result = analyse_log(str(log_file))

    assert result["time_range"] == {
        "start": "2026-10-28T10:00:00",
        "end": "2026-10-28T10:05:00",
    }


def test_empty_log_file(tmp_path: Path) -> None:
    log_file = tmp_path / "empty.log"

    log_file.write_text("", encoding="utf-8")

    result = analyse_log(str(log_file))

    assert result["counts_by_level"] == {}
    assert result["top_errors"] == []
    assert result["time_range"] == {
        "start": None,
        "end": None,
    }
    assert result["bad_lines"] == 0


def test_missing_log_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.log"

    with pytest.raises(LogFileError):
        analyse_log(str(missing_file))
