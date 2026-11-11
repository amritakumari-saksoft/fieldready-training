"""Application dependency readiness checks."""

import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import engine

logger = logging.getLogger(__name__)


def check_database() -> bool:
    """Check whether PostgreSQL is available."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except SQLAlchemyError as exc:
        logger.warning(
            "Database readiness check failed: %s",
            type(exc).__name__,
        )
        return False


def check_dependencies() -> list[str]:
    """Return unavailable application dependencies."""

    problems: list[str] = []

    if not check_database():
        problems.append("database_unavailable")

    return problems


def check_readiness() -> tuple[bool, list[str]]:
    """Return readiness status and dependency problems."""

    problems = check_dependencies()

    return not problems, problems
