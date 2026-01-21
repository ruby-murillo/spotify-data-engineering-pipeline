from datetime import datetime, date

def extract_mock(run_id: str):
    extracted_at = datetime.utcnow()
    return [
        {
            "run_id": run_id,
            "extracted_at": extracted_at,
            "track_id": "mock_001",
            "track_name": "Blinding Lights",
            "artist_name": "The Weeknd",
            "album_name": "After Hours",
            "release_date": date(2019, 11, 29),
            "popularity": 95,
            "duration_ms": 200040,
            "source": "mock",
        },
        {
            "run_id": run_id,
            "extracted_at": extracted_at,
            "track_id": "mock_002",
            "track_name": "bad guy",
            "artist_name": "Billie Eilish",
            "album_name": "WHEN WE ALL FALL ASLEEP, WHERE DO WE GO?",
            "release_date": date(2019, 3, 29),
            "popularity": 90,
            "duration_ms": 194088,
            "source": "mock",
        },
    ]