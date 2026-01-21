import os
import sys
 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(SRC_DIR)
 
from utils.db import get_conn
 
SQL = """
CREATE SCHEMA IF NOT EXISTS analytics;
 
-- Track-level metrics (simple but useful)
DROP TABLE IF EXISTS analytics.track_metrics;
CREATE TABLE analytics.track_metrics AS
SELECT
    track_id,
    track_name,
    artist_name,
    album_name,
    release_date,
    popularity,
    duration_ms,
    source,
    extracted_at
FROM clean.tracks;
 
CREATE UNIQUE INDEX IF NOT EXISTS ux_track_metrics_track_id
ON analytics.track_metrics (track_id);
 
-- Artist-level rollup metrics (interview-friendly)
DROP TABLE IF EXISTS analytics.artist_track_metrics;
CREATE TABLE analytics.artist_track_metrics AS
SELECT
    artist_name,
    COUNT(*) AS track_count,
    AVG(popularity)::numeric(10,2) AS avg_popularity,
    MIN(popularity) AS min_popularity,
    MAX(popularity) AS max_popularity,
    AVG(duration_ms)::numeric(12,2) AS avg_duration_ms
FROM clean.tracks
GROUP BY artist_name;
 
CREATE UNIQUE INDEX IF NOT EXISTS ux_artist_track_metrics_artist
ON analytics.artist_track_metrics (artist_name);
"""
 
def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
        conn.commit()
 
if __name__ == "__main__":
    run()