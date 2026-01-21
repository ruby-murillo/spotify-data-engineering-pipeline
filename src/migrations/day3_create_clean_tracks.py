"""
Day 3 Migration
Creates a canonical clean layer for tracks.

Primary (B): clean.tracks (physical table)
Also (A):     clean.tracks_vw (view using same logic)

Assumptions based on Day 2:
- Source table is raw.tracks_mock
- We choose ONE row per track_id (canonical record).
- If multiple sources exist for same track_id, we prefer:
    1) latest extracted_at
    2) source priority: json > csv > mock (tie-breaker)
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(SRC_DIR)

from utils.db import get_conn

RAW_TABLE = "raw.tracks_mock"
CLEAN_SCHEMA = "clean"
CLEAN_TABLE = "clean.tracks"
CLEAN_VIEW = "clean.tracks_vw"

SQL = f"""
-- 1) schema
CREATE SCHEMA IF NOT EXISTS {CLEAN_SCHEMA};

-- 2) physical table (B)
DROP TABLE IF EXISTS {CLEAN_TABLE};

CREATE TABLE {CLEAN_TABLE} AS
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.track_id
            ORDER BY
                t.extracted_at DESC NULLS LAST,
                CASE t.source
                    WHEN 'json' THEN 1
                    WHEN 'csv'  THEN 2
                    WHEN 'mock' THEN 3
                    ELSE 9
                END ASC
        ) AS rn
    FROM {RAW_TABLE} t
   WHERE track_id IS NOT NULL
)
SELECT
    run_id,
    extracted_at,
    track_id,
    track_name,
    artist_name,
    album_name,
    release_date,
    popularity,
    duration_ms,
    source
FROM ranked
WHERE rn = 1;

-- 3) enforce canonical uniqueness (portfolio-friendly)
CREATE UNIQUE INDEX IF NOT EXISTS ux_clean_tracks_track_id
ON {CLEAN_TABLE} (track_id);

-- 4) view (A) - same logic, non-materialized
DROP VIEW IF EXISTS {CLEAN_VIEW};

CREATE VIEW {CLEAN_VIEW} AS
WITH ranked AS (
    SELECT
        t.*,
        ROW_NUMBER() OVER (
            PARTITION BY t.track_id
            ORDER BY
                t.extracted_at DESC NULLS LAST,
                CASE t.source
                    WHEN 'json' THEN 1
                    WHEN 'csv'  THEN 2
                    WHEN 'mock' THEN 3
                    ELSE 9
                END ASC
        ) AS rn
    FROM {RAW_TABLE} t
   WHERE track_id IS NOT NULL
)
SELECT
    run_id,
    extracted_at,
    track_id,
    track_name,
    artist_name,
    album_name,
    release_date,
    popularity,
    duration_ms,
    source
FROM ranked
WHERE rn = 1;
"""

def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
        conn.commit()

if __name__ == "__main__":
    run()