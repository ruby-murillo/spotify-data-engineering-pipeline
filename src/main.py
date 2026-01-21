import uuid
from dotenv import load_dotenv
from utils.file_extract import extract_from_files
from utils.db import insert_tracks, get_conn

def main():
    load_dotenv()
    run_id = str(uuid.uuid4())

    rows = extract_from_files(run_id=run_id)
    insert_tracks(rows)

    print(f"Loaded {len(rows)} rows into raw.tracks_mock (run_id={run_id})")

    # --- Day 2 QA: counts by source ---
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT source, COUNT(*) 
                FROM raw.tracks_mock
                GROUP BY source
                ORDER BY source;
            """)
            results = cur.fetchall()

    print("Counts by source:")
    for source, cnt in results:
        print(f"{source}: {cnt}")

if __name__ == "__main__":
    main()