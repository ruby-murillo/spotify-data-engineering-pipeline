import os
import sys
 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)
 
from utils.db import get_conn
 
CHECKS = {
    "clean_tracks_rowcount": """
        SELECT COUNT(*) FROM clean.tracks;
    """,
    "analytics_tracks_rowcount": """
        SELECT COUNT(*) FROM analytics.track_metrics;
    """,
    "duplicate_track_ids": """
        SELECT track_id, COUNT(*) 
        FROM analytics.track_metrics
        GROUP BY track_id
        HAVING COUNT(*) > 1;
    """,
    "null_track_ids": """
        SELECT COUNT(*) 
        FROM analytics.track_metrics
        WHERE track_id IS NULL;
    """,
    "popularity_range": """
        SELECT MIN(popularity), MAX(popularity)
        FROM analytics.track_metrics;
    """
}
 
def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            for name, sql in CHECKS.items():
                print(f"\n--- {name} ---")
                cur.execute(sql)
                for row in cur.fetchall():
                    print(row)
 
if __name__ == "__main__":
    run()