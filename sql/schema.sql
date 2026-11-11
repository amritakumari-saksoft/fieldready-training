
-- sql/schema.sql
-- Day 7: Variant 3 - Parcels
-- Canonical database schema

-- Table 1: Parcel categories
CREATE TABLE IF NOT EXISTS categories (
    category_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Table 2: Parcels
CREATE TABLE IF NOT EXISTS parcels (
    parcel_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    category_id BIGINT NOT NULL
        REFERENCES categories(category_id),
    created_at DATE NOT NULL,

    CONSTRAINT chk_parcel_status
        CHECK (status IN ('active', 'inactive', 'pending'))
);

-- Table 3: Parcel status history
CREATE TABLE IF NOT EXISTS parcel_events (
    event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parcel_id BIGINT NOT NULL
        REFERENCES parcels(parcel_id) ON DELETE CASCADE,
    status TEXT NOT NULL,
    event_time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index 1: Speeds up filtering parcels by status.
CREATE INDEX IF NOT EXISTS idx_parcels_status
    ON parcels(status);

-- Index 2: Speeds up joins and filtering by category.
CREATE INDEX IF NOT EXISTS idx_parcels_category
    ON parcels(category_id);

-- Index 3: Speeds up fetching a parcel's events by time.
CREATE INDEX IF NOT EXISTS idx_events_parcel_time
    ON parcel_events(parcel_id, event_time);
