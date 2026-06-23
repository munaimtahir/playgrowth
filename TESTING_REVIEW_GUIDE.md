# Testing and Review Guide for PlayGrowth Copilot MVP

This document outlines how an agent should test and review the MVP of PlayGrowth Copilot to ensure it follows the stage gate rules and prevents accidental "production write" automation actions.

## 1. Initial Scaffold and Health Checks

1. Verify Docker Compose setup:
   ```bash
   docker compose build
   docker compose up -d
   ```
2. Verify all services start:
   ```bash
   docker compose ps
   curl -f http://localhost:8000/api/health/
   curl -f http://localhost:5173/
   ```
3. Verify backend tests pass:
   ```bash
   docker compose exec backend python manage.py test
   ```

## 2. Seed Data and Data Imports

1. Ensure the management command successfully runs and is idempotent:
   ```bash
   docker compose exec backend python manage.py seed_arcade_app
   ```
2. Ensure the CSV templates are present:
   ```bash
   ls data/templates/
   ```
3. Test imports. Verify the system can import basic data from the templates:
   ```bash
   curl -f -X POST http://localhost:8000/api/v1/imports/daily-metrics/ -F "app=1" -F "file=@data/templates/daily_metrics.csv"
   curl -f -X POST http://localhost:8000/api/v1/imports/reviews/ -F "app=1" -F "file=@data/templates/reviews.csv"
   curl -f -X POST http://localhost:8000/api/v1/imports/android-vitals/ -F "app=1" -F "file=@data/templates/android_vitals.csv"
   curl -f -X POST http://localhost:8000/api/v1/imports/ads/ -F "app=1" -F "file=@data/templates/ads.csv"
   ```

## 3. Verify App Logic

1. Verify Dashboard summary and deterministic diagnosis:
   ```bash
   curl -f "http://localhost:8000/api/v1/dashboard/summary/?app=1&start=2026-06-01&end=2026-06-21"
   ```
2. Verify mock AI Provider doesn't use API keys, and test growth reports generation:
   ```bash
   curl -f -X POST http://localhost:8000/api/v1/growth-reports/generate/ -H "Content-Type: application/json" -d '{"app":1,"period_start":"2026-06-01","period_end":"2026-06-21","report_type":"weekly"}'
   ```
3. Verify listing advisors generation:
   ```bash
   curl -f -X POST "http://localhost:8000/api/v1/listing-advisor/generate/" -H "Content-Type: application/json" -d '{"app":1}'
   ```
4. Check that state transitions on Recommendations do not execute external scripts:
   ```bash
   curl -f -X POST http://localhost:8000/api/v1/recommendations/1/accept/
   curl -f -X POST http://localhost:8000/api/v1/recommendations/1/mark-implemented/
   curl -f -X POST http://localhost:8000/api/v1/recommendations/1/close/
   ```

## 4. Safety Scan

The most critical review is to ensure there are absolutely no automatic Play Console write operations. The copilot recommends and the developer decides.
Run this script to verify:
```bash
grep -RniE "publish to play|upload screenshots|increase ads budget|launch campaign|reply automatically|auto publish|auto reply|play console write|google ads write|firebase write|production write" . \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude-dir=.venv \
  --exclude-dir=venv || true
```

If it returns anything that interacts directly with any production API (like Play Console, or Ads APIs) with the capability of writing changes automatically, it is a **failure**.
