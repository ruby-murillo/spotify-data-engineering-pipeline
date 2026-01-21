from dotenv import load_dotenv
from src.utils.db import get_conn
 
DDL = """
ALTER TABLE raw.tracks_mock
ADD CONSTRAINT tracks_mock_track_id_source_uk UNIQUE (track_id, source);
"""
 
def main():
    load_dotenv()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
        conn.commit()
    print("OK: added UNIQUE(track_id, source) on raw.tracks_mock")
 
if __name__ == "__main__":
    main()