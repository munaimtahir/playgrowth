# Staged Implementation Roadmap — PlayGrowth Copilot v2

## Stage 0 — Repository Foundation

Goal:
Create a clean monorepo scaffold.

Tasks:

- Create Docker Compose setup.
- Create Django backend.
- Create Vite React frontend.
- Add PostgreSQL, Redis, Celery.
- Add `.env.example`.
- Add base README.
- Add `/docs` folder with this dev pack.

Exit criteria:

- `docker compose up --build` starts backend, frontend, database, and Redis.
- Backend health endpoint works.
- Frontend loads.

## Stage 1 — Core Backend Models

Goal:
Implement the manual-data domain.

Tasks:

- AppProfile model
- DailyMetric model
- ReviewItem model
- AndroidVitalsMetric model
- AdCampaignMetric model
- StoreListingSnapshot model
- GrowthReport model
- Recommendation model
- Experiment model
- ManualActionLog model
- AuditLog model
- DRF serializers/viewsets
- Admin registration

Exit criteria:

- CRUD endpoints work.
- Admin can create seed app.

## Stage 2 — Manual Data Import

Goal:
Make MVP useful without APIs.

Tasks:

- Manual daily metric form endpoint
- CSV import for daily metrics
- CSV import for reviews
- Import batch tracking
- CSV template files
- Basic validation errors

Exit criteria:

- User can import 7–30 days of metrics.
- User can import review rows.

## Stage 3 — Dashboard

Goal:
Show growth state.

Tasks:

- Dashboard summary endpoint
- KPI cards
- Growth trend chart
- Data freshness warnings
- Top recommendation panel

Exit criteria:

- Dashboard shows installs, visitors, conversion, retention, ratings, crashes, ads.

## Stage 4 — Diagnosis Engine

Goal:
Add deterministic bottleneck logic.

Tasks:

- Rule-based diagnosis service
- Bottleneck labels
- Evidence extraction
- Confidence scoring
- Unit tests

Exit criteria:

- System can identify discovery, conversion, retention, quality, review, or ads bottlenecks.

## Stage 5 — AI Service Layer

Goal:
Add provider-abstracted AI.

Tasks:

- Base AIProvider class
- MockAIProvider for development
- Prompt builder
- GrowthAnalysisService
- ListingAdvisorService
- ReviewAnalysisService
- ExperimentPlannerService
- SafetyPolicyService

Exit criteria:

- App can generate a report without external AI keys using mock provider.
- Later providers can be added without changing views.

## Stage 6 — Recommendations and Action Log

Goal:
Turn diagnosis into human action.

Tasks:

- Recommendation card UI
- Status transitions
- Create manual action from recommendation
- Action log UI
- Outcome notes

Exit criteria:

- User can accept/reject/implement/monitor recommendations.
- No external system is changed.

## Stage 7 — Review Analyzer

Goal:
Make reviews actionable.

Tasks:

- Import reviews
- Classify reviews
- Generate themes
- Draft manual replies
- Suggest product fixes

Exit criteria:

- Reviews become themes and recommendations.

## Stage 8 — Listing Advisor and Experiment Planner

Goal:
Support Play Store improvement without automation.

Tasks:

- Current listing snapshot form
- Short description generator
- Screenshot caption ideas
- Feature graphic ideas
- Experiment builder

Exit criteria:

- User gets copyable listing suggestions and structured experiments.

## Stage 9 — Internal Use on Offline Mini Arcade

Goal:
Use the product on the real launched game.

Tasks:

- Add real app profile.
- Add current listing snapshot.
- Import first 7–30 days of metrics.
- Import first reviews if available.
- Generate first report.
- Create first three recommendations.
- Log actual manual changes.

Exit criteria:

- The system produces a practical next-action plan for the arcade game.

## Later Stages — Read-Only Integrations

Only after MVP manual workflow works:

1. Google Play report import
2. Review fetch
3. Android vitals read
4. Firebase/GA4 read
5. Google Ads read

Write integrations remain out of scope unless a future product decision intentionally reopens them.
