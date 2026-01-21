import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)
from utils.db import get_conn

SQLS = {
    "null_in_analytics": """
        SELECT track_id, track_name, artist_name, album_name, source, extracted_at
        FROM analytics.track_metrics
        WHERE track_id IS NULL;
    """,
    "null_in_clean": """
        SELECT track_id, track_name, artist_name, album_name, source, extracted_at
        FROM clean.tracks
        WHERE track_id IS NULL;
    """,
}

def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            for name, sql in SQLS.items():
                print(f"\n--- {name} ---")
                cur.execute(sql)
                rows = cur.fetchall()
                if not rows:
                    print("(no rows)")
                else:
                    for r in rows:
                        print(r)

if __name__ == "__main__":
    run()