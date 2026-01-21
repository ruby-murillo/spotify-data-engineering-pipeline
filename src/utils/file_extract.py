import csv
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any
 
 
def _utc_now_iso() -> str:
    # Example: 2026-01-16T18:05:12Z
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
 
 
def _normalize_track(row: Dict[str, Any], run_id: str, source: str) -> Dict[str, Any]:
    """
    Convert an input row (from JSON/CSV) into the dict format expected by utils.db.insert_tracks().
    """
    # Defensive parsing helpers
    def to_int(v):
        if v is None or v == "":
            return None
        try:
            return int(v)
        except Exception:
            return None
 
    return {
        "run_id": run_id,
        "extracted_at": _utc_now_iso(),
        "track_id": row.get("track_id"),
        "track_name": row.get("track_name"),
        "artist_name": row.get("artist_name"),
        "album_name": row.get("album_name"),
        "release_date": row.get("release_date"),
        "popularity": to_int(row.get("popularity")),
        "duration_ms": to_int(row.get("duration_ms")),
        "source": source,
    }
 
 
def extract_from_files(
    run_id: str,
    json_path: str = os.path.join("data", "day2", "input", "json", "tracks.json"),
    csv_path: str = os.path.join("data", "day2", "input", "csv", "tracks.csv"),
) -> List[Dict[str, Any]]:
    """
    Reads Day 2 JSON + CSV and returns a single list of normalized track rows.
    """
    rows: List[Dict[str, Any]] = []
 
    # --- JSON ---
    with open(json_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"JSON input must be a list of objects. Got: {type(data)}")
        for obj in data:
            if not isinstance(obj, dict):
                continue
            rows.append(_normalize_track(obj, run_id=run_id, source="json"))
 
    # --- CSV ---
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for obj in reader:
            rows.append(_normalize_track(obj, run_id=run_id, source="csv"))
 
    return rows