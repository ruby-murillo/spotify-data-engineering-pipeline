# Spotify Data Engineering Portfolio
 
## Problem
Raw music data arrives from multiple sources and formats, creating challenges
around duplication, consistency, and analytics readiness.
 
## Design
The pipeline was designed in layered stages:
- Raw ingestion (CSV, JSON, mock data)
- Clean canonical layer with deterministic deduplication
- Analytics layer optimized for business consumption
 
## Key Decisions
- Materialized clean tables for stability and performance
- Window-function-based deduplication
- Explicit QA checks at each stage
- Analytics tables separated from clean layer
 
## Data Quality & Validation
- Rowcount parity checks
- Duplicate key detection
- Null key detection
- Metric range sanity checks
 
## Outcomes
- One-row-per-entity clean dataset
- Dashboard-ready analytics tables
- Reproducible, logged pipeline runs
 
## What I’d Do Next
- Incremental processing using run_id
- Partitioning analytics tables
- Automated alerts on QA thresholds