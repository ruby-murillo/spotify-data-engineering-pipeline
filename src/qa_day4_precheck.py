import os
import sys
 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)
 
from utils.db import get_conn
 
SQLS = {
    "clean_schema_exists": """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name = 'clean';
    """,
    "clean_tracks_exists": """
        SELECT to_regclass('clean.tracks');
    """,
    "clean_tracks_rowcount": """
        SELECT COUNT(*) FROM clean.tracks;
    """,
}
 
def run():
    with get_conn() as conn:
        with conn.cursor() as cur:
            for name, sql in SQLS.items():
                print(f"\n--- {name} ---")
                cur.execute(sql)
                for row in cur.fetchall():
                    print(row)
 
if __name__ == "__main__":
    run()