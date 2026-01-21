-- Top artists by average popularity
SELECT
    artist_name,
    track_count,
    avg_popularity
FROM analytics.artist_track_metrics
ORDER BY avg_popularity DESC
LIMIT 10;
 
-- Longest tracks with high popularity
SELECT
    track_name,
    artist_name,
    duration_ms,
    popularity
FROM analytics.track_metrics
WHERE popularity >= 80
ORDER BY duration_ms DESC
LIMIT 10;
 
-- Artist catalog size vs popularity
SELECT
    artist_name,
    track_count,
    avg_popularity
FROM analytics.artist_track_metrics
ORDER BY track_count DESC
LIMIT 10;