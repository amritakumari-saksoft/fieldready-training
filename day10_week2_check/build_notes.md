# Build Notes

## Dependencies
Added psycopg[binary]>=3.3.7 to pyproject.toml.

Updated uv.lock using the dependency resolver.

## Database
PostgreSQL 17 is running in Docker.

Database: parcels_db

Existing tables:
- categories
- parcels
- parcel_events

## Validation
- psycopg version: 3.3.7
- pg_isready: accepting connections
- git diff --check: passed

## Notes
The database schema is maintained in sql/schema.sql.
