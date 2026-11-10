"""Readiness checks for service dependencies."""

import logging

import psycopg

from app.config import get_settings

logger = logging.getLogger(__name__)


def check_dependencies() -> list[str]:
    """Return dependency problems. An empty list means ready."""
    settings = get_settings()

    try:
        with (
            psycopg.connect(
                host=settings.postgres_host,
                port=settings.postgres_port,
                dbname=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password.get_secret_value(),
                connect_timeout=3,
            ) as connection,
            connection.cursor() as cursor,
        ):
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

            if result != (1,):
                return ["Database health check failed"]

    except psycopg.Error as exc:
        logger.warning(
            "Database readiness check failed: %s",
            type(exc).__name__,
        )
        return ["Database unavailable"]

    return []
