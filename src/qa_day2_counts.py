from dotenv import load dotenv
from utils.db import get_conn

SQL = """
SELECT source, COUNT(*) AS cnt
FROM raw.tracks_mock
GROUP BY source
ORDER BY source;
"""

def main():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(SQL)
            rows = cur.fetchall()

    print("Counts by source:")
    for source, cnt in rows:
        print(f"{source}\t{cnt}")

if __name__ == "__main__":
    main()