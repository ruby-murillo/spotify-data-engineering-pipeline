import os
from pathlib import Path
import matplotlib.pyplot as plt

# Reuse your existing DB connection helper
from src.utils.db import get_conn

OUTDIR = Path("reports") / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

def fetch_all(query: str, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()

def plot_popularity_hist():
    rows = fetch_all("""
        SELECT popularity
        FROM analytics.track_metrics
        WHERE popularity IS NOT NULL
   """)
    popularity = [r[0] for r in rows if r[0] is not None]

    plt.figure()
    plt.hist(popularity, bins=10)
    plt.title("Track Popularity Distribution")
    plt.xlabel("Popularity")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(OUTDIR / "popularity_distribution.png", dpi=200)
    plt.close()

def plot_top_artists():
    rows = fetch_all("""
        SELECT artist_name, COUNT(*) AS track_count
        FROM analytics.track_metrics
        WHERE artist_name IS NOT NULL AND artist_name <> ''
        GROUP BY 1
        ORDER BY track_count DESC, artist_name
        LIMIT 10
    """)
    artists = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure()
    plt.barh(artists[::-1], counts[::-1])  # reverse so #1 shows at top
    plt.title("Top 10 Artists by Track Count")
    plt.xlabel("Track Count")
    plt.ylabel("Artist")
    plt.tight_layout()
    plt.savefig(OUTDIR / "top_artists_track_count.png", dpi=200)
    plt.close()

def main():
    plot_popularity_hist()
    plot_top_artists()
    print(f"Saved charts to: {OUTDIR}")

if __name__ == "__main__":
    main()