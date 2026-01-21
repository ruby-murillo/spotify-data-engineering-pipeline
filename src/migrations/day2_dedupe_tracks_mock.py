from dotenv import load_dotenv
from src.utils.db import get_conn

SQL = """
DELETE FROM raw.tracks_mock t
USING raw.tracks_mock d
WHERE t.track_id = d.track_id
  AND t.source   = d.source
  AND t.extracted_at < d.extracted_at;
"""

def main():
    load_dotenv()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
            deleted = cur.rowcount
        conn.commit()

    print(f"OK: deduped raw.tracks_mock (deleted {deleted} duplicate rows)")

if __name__ == "__main__":
    main()