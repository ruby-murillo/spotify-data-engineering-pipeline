import os
import sys
 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)
 
from utils.db import get_conn
 
QA = {
    "track_metrics_rowcount": "SELECT COUNT(*) FROM analytics.track_metrics;",
    "clean_tracks_rowcount": "SELECT COUNT(*) FROM clean.tracks;",
    "track_metrics_dupes": """
        SELECT track_id, COUNT(*) AS n
        FROM analytics.track_metrics
        GROUP BY track_id
        HAVING COUNT(*) > 1
        LIMIT 20;
    """,
    "artist_metrics_rowcount": "SELECT COUNT(*) FROM analytics.artist_track_metrics;",
    "artist_metrics_null_artist": "SELECT COUNT(*) FROM analytics.artist_track_metrics WHERE artist_name IS NULL;",
    "popularity_range_check": """
        SELECT
            MIN(popularity) AS min_popularity,
            MAX(popularity) AS max_popularity
        FROM analytics.track_metrics;
    """,
}
 
def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            for name, sql in QA.items():
                print(f"\n--- {name} ---")
                cur.execute(sql)
                rows = cur.fetchall()
                for r in rows:
                    print(r)
 
if __name__ == "__main__":
    run()