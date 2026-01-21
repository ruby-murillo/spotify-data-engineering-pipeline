import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# Load .env from project root (reliable on Windows)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )


def insert_tracks(rows):
    cols = [
        "run_id", "extracted_at", "track_id", "track_name", "artist_name",
        "album_name", "release_date", "popularity", "duration_ms", "source"
    ]
    values = [[r.get(c) for c in cols] for r in rows]

    sql = f"""
          INSERT INTO raw.tracks_mock ({','.join(cols)})
          VALUES %s
          ON CONFLICT (track_id, source) DO NOTHING
          """


    with get_conn() as conn:
        with conn.cursor() as cur:
           execute_values(cur, sql, values)
        conn.commit()
