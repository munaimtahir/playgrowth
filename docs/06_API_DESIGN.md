# API Design — PlayGrowth Copilot v2

Base path:

```text
/api/v1/
```

## 1. App Profiles

```http
GET    /api/v1/apps/
POST   /api/v1/apps/
GET    /api/v1/apps/{id}/
PATCH  /api/v1/apps/{id}/
DELETE /api/v1/apps/{id}/
```

## 2. Metrics

```http
GET    /api/v1/daily-metrics/?app={id}&start=YYYY-MM-DD&end=YYYY-MM-DD
POST   /api/v1/daily-metrics/
PATCH  /api/v1/daily-metrics/{id}/
DELETE /api/v1/daily-metrics/{id}/
```

## 3. CSV Imports

```http
POST /api/v1/imports/daily-metrics/
POST /api/v1/imports/reviews/
POST /api/v1/imports/android-vitals/
POST /api/v1/imports/ads/
GET  /api/v1/import-batches/
```

MVP implementation can start with daily metrics and reviews only, then add others.

## 4. Reviews

```http
GET    /api/v1/reviews/?app={id}
POST   /api/v1/reviews/
PATCH  /api/v1/reviews/{id}/
POST   /api/v1/reviews/analyze/?app={id}
GET    /api/v1/review-themes/?app={id}
```

## 5. Listing Snapshots

```http
GET    /api/v1/listing-snapshots/?app={id}
POST   /api/v1/listing-snapshots/
PATCH  /api/v1/listing-snapshots/{id}/
POST   /api/v1/listing-advisor/generate/?app={id}
```

## 6. Growth Reports

```http
GET  /api/v1/growth-reports/?app={id}
POST /api/v1/growth-reports/generate/
GET  /api/v1/growth-reports/{id}/
```

Generate report request:

```json
{
  "app": 1,
  "period_start": "2026-06-01",
  "period_end": "2026-06-21",
  "report_type": "weekly"
}
```

## 7. Recommendations

```http
GET   /api/v1/recommendations/?app={id}&status=suggested
POST  /api/v1/recommendations/
PATCH /api/v1/recommendations/{id}/
POST  /api/v1/recommendations/{id}/accept/
POST  /api/v1/recommendations/{id}/reject/
POST  /api/v1/recommendations/{id}/mark-implemented/
POST  /api/v1/recommendations/{id}/close/
```

No endpoint should execute an external Play Console or Google Ads change.

## 8. Experiments

```http
GET    /api/v1/experiments/?app={id}
POST   /api/v1/experiments/
PATCH  /api/v1/experiments/{id}/
POST   /api/v1/experiments/from-recommendation/{recommendation_id}/
```

## 9. Manual Action Logs

```http
GET    /api/v1/manual-actions/?app={id}
POST   /api/v1/manual-actions/
PATCH  /api/v1/manual-actions/{id}/
```

## 10. Dashboard Summary

```http
GET /api/v1/dashboard/summary/?app={id}&start=YYYY-MM-DD&end=YYYY-MM-DD
```

Response:

```json
{
  "kpis": {
    "installs": 120,
    "store_visitors": 900,
    "conversion_rate": 13.3,
    "day_1_retention": 22.5,
    "crash_rate": 0.4
  },
  "bottleneck": "Store conversion problem",
  "top_recommendations": [],
  "recent_actions": []
}
```
