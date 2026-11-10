"""PostgreSQL database connection and engine configuration."""

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine

from app.config import get_settings


def create_database_engine() -> Engine:
    """Create a PostgreSQL engine using application settings."""

    settings = get_settings()

    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=settings.postgres_db,
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


engine = create_database_engine()
