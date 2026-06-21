# Coding Agent Prompt — Build PlayGrowth Copilot MVP-0

You are working inside the `playgrowth-copilot` repository.

## Product Direction

Build PlayGrowth Copilot as an AI-assisted growth analyst for Android app developers.

This is not an autonomous growth bot. Do not implement any feature that directly changes Google Play Console, Google Ads, Firebase, Play Store listings, screenshots, titles, budgets, reviews, or production publishing.

The product must track data, diagnose issues, generate recommendations, draft copyable suggestions, and log manual actions taken by the developer.

## MVP Stack

- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Docker Compose
- Vite React
- TypeScript
- Tailwind CSS
- Recharts

## Build Priorities

### 1. Repository Setup

Create or maintain this structure:

```text
playgrowth-copilot/
  backend/
  frontend/
  docs/
  data/templates/
  docker-compose.yml
  .env.example
  README.md
```

### 2. Backend

Implement:

- AppProfile
- DataImportBatch
- DailyMetric
- CountryMetric
- StoreListingSnapshot
- ReviewItem
- ReviewTheme
- AndroidVitalsMetric
- AdCampaignMetric
- GrowthReport
- Recommendation
- Experiment
- ManualActionLog
- AuditLog

Add:

- DRF serializers
- ViewSets
- Router URLs
- Admin registration
- Dashboard summary endpoint
- Report generation endpoint
- CSV import endpoints for daily metrics and reviews first

### 3. Diagnosis Engine

Create a deterministic service that identifies:

- discovery problem
- store conversion problem
- retention problem
- quality/stability problem
- review/theme problem
- ads efficiency problem
- insufficient data

Return evidence, confidence, and recommended next metric to watch.

### 4. AI Layer

Create an abstract AI provider layer:

- BaseAIProvider
- MockAIProvider
- AIServiceRouter
- PromptBuilder

Do not hardcode provider-specific logic into views.

MVP should work without an API key using MockAIProvider.

### 5. Frontend

Implement screens:

- Dashboard
- App Profile
- Data Import
- Growth Reports
- Recommendations
- Reviews
- Listing Advisor
- Experiments
- Action Log
- Settings

### 6. Safety Requirements

The UI must not include buttons like:

- Publish to Play Console
- Increase Ads Budget
- Launch Campaign
- Upload Screenshots
- Reply Automatically
- Change App Title Automatically

Allowed button language:

- Copy suggestion
- Mark as accepted
- Mark as manually implemented
- Create action log
- Start manual experiment
- Export report

### 7. Initial Seed App

Add a management command to seed:

- App name: Offline Mini Arcade
- Games: Pulse Orbit, Lane Drift, Stack Drop
- Positioning: lightweight, offline-first, quick arcade sessions, low-end Android friendly, honest listing, no aggressive monetization

### 8. Exit Criteria

The MVP is acceptable when:

- Docker Compose starts.
- Backend health endpoint works.
- Frontend loads.
- Seed data can be created.
- App profile is visible.
- Daily metrics can be added/imported.
- Reviews can be added/imported.
- Dashboard shows KPI cards.
- Diagnosis engine generates bottleneck.
- Recommendations can be generated and status-tracked.
- Manual actions can be logged.
- No external production write automation exists.
