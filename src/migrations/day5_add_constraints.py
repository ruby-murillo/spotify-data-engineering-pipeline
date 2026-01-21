import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(SRC_DIR)
from utils.db import get_conn

SQL = """
ALTER TABLE analytics.track_metrics
  ALTER COLUMN track_id SET NOT NULL;
"""

def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
        conn.commit()

if __name__ == "__main__":
    run()