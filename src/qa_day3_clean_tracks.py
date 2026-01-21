import os
import sys

# Ensure src/ is on the path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from utils.db import get_conn

QA_SQLS = {
    "raw_rowcount": "SELECT COUNT(*) FROM raw.tracks_mock;",
    "clean_rowcount": "SELECT COUNT(*) FROM clean.tracks;",
    "clean_distinct_track_id": "SELECT COUNT(DISTINCT track_id) FROM clean.tracks;",
    "clean_dupes_track_id": """
        SELECT track_id, COUNT(*) AS n
        FROM clean.tracks
        GROUP BY track_id
        HAVING COUNT(*) > 1
        ORDER BY n DESC
        LIMIT 20;
    """,
    "clean_null_track_id": "SELECT COUNT(*) FROM clean.tracks WHERE track_id IS NULL;",
}

def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            for name, sql in QA_SQLS.items():
                print(f"\n--- {name} ---")
                cur.execute(sql)
                rows = cur.fetchall()
                for r in rows:
                    print(r)

if __name__ == "__main__":
    run()