import logging
from collections import Counter
from datetime import datetime
from pathlib import Path

from exceptions import LogFileError
from models import LogEntry

logger = logging.getLogger(__name__)


def analyse_log(file_path: str) -> dict[str, object]:
    counts: Counter[str] = Counter()
    errors: Counter[str] = Counter()
    timestamps: list[datetime] = []
    bad_lines = 0

    logger.info("Starting log analysis: %s", file_path)

    try:
        with Path(file_path).open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                parts = line.strip().split(maxsplit=3)

                if len(parts) != 4:
                    bad_lines += 1
                    logger.warning("Invalid log at line %d", line_number)
                    continue

                date, time, level, message = parts

                try:
                    timestamp = datetime.fromisoformat(f"{date} {time}")
                except ValueError:
                    bad_lines += 1
                    logger.warning(
                        "Invalid timestamp at line %d",
                        line_number,
                    )
                    continue

                if level not in {"INFO", "WARNING", "ERROR"}:
                    bad_lines += 1
                    logger.warning(
                        "Invalid level at line %d",
                        line_number,
                    )
                    continue

                entry = LogEntry(timestamp, level, message)
                counts[entry.level] += 1
                timestamps.append(entry.timestamp)

                if entry.level == "ERROR":
                    errors[entry.message] += 1

    except OSError as exc:
        logger.error("Cannot read log file: %s", file_path)
        raise LogFileError(f"Cannot read log file: {file_path}") from exc

    logger.info("Log analysis completed")

    return {
        "counts_by_level": dict(counts),
        "top_errors": [
            {"message": message, "count": count} for message, count in errors.most_common(5)
        ],
        "time_range": {
            "start": min(timestamps).isoformat() if timestamps else None,
            "end": max(timestamps).isoformat() if timestamps else None,
        },
        "bad_lines": bad_lines,
    }
