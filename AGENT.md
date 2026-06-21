# AGENTS.md — PlayGrowth Copilot AI Coding Guidance

## 1. Project Identity

You are working inside the `playgrowth-copilot` repository.

**PlayGrowth Copilot** is an AI-assisted growth analyst for Android app developers. It helps a developer understand app growth problems using manual/imported app data, reviews, store-listing snapshots, Android vitals summaries, ads summaries, experiments, and manual action logs.

The product behaves like a careful growth consultant.

It is **not** an autonomous marketing bot.

Core principle:

> PlayGrowth Copilot recommends. The developer decides and implements.

Initial internal app:

- App: Offline Mini Arcade
- Games: Pulse Orbit, Lane Drift, Stack Drop
- Positioning: lightweight, offline-first, quick arcade sessions, low-end Android friendly, honest listing, no aggressive monetization

---

## 2. Non-Negotiable Safety Rules

Never implement any feature that directly changes, publishes, uploads, replies, budgets, launches, or edits production assets in:

- Google Play Console
- Google Ads
- Firebase
- Play Store listing
- App screenshots
- App title
- App description
- App releases
- Review replies
- Ad budgets
- Campaign settings

### Forbidden UI/Button Labels

Do not add buttons or menu items named:

- Publish to Play Console
- Increase Ads Budget
- Launch Campaign
- Upload Screenshots
- Reply Automatically
- Change App Title Automatically
- Auto Optimize
- Auto Publish
- Auto Reply
- Execute Recommendation

### Allowed UI/Button Labels

Use manual, human-controlled language:

- Copy suggestion
- Mark as accepted
- Mark as rejected
- Mark as manually implemented
- Create action log
- Start manual experiment
- Export report
- Generate report
- Analyze reviews
- Generate listing suggestions
- Save draft
- Record manual change

### Safety Scan Requirement

After every meaningful stage, run a repository safety scan:

```bash
grep -RniE "publish to play|upload screenshots|increase ads budget|launch campaign|reply automatically|auto publish|auto reply|play console write|google ads write|firebase write|production write|execute recommendation" . \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude-dir=venv \
  --exclude-dir=.venv || true
```

If a match is found in documentation as a warning, it is acceptable. If a match is found as a real feature, endpoint, service, or UI action, remove or rename it.

---

## 3. Required Stack

Backend:

- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- django-cors-headers
- django-filter

Frontend:

- Vite
- React
- TypeScript
- Tailwind CSS
- React Router
- Recharts

Deployment:

- Docker Compose
- Backend container
- Frontend container
- PostgreSQL container
- Redis container
- Celery worker container
- Optional Celery beat container
- `.env` file
- `.env.example`

AI layer:

- Provider abstraction
- Mock provider for MVP
- Optional later providers for OpenAI, Gemini, or local model services
- MVP must work without real AI API keys using `MockAIProvider`

---

## 4. Expected Repository Structure

Maintain or create this structure:

```text
playgrowth-copilot/
  backend/
    manage.py
    requirements.txt
    Dockerfile
    config/
    apps/
      growth/
      ai/
      imports/
      reports/
  frontend/
    package.json
    Dockerfile
    src/
      api/
      components/
      layouts/
      pages/
      routes/
      types/
  docs/
  data/
    templates/
  docker-compose.yml
  .env.example
  README.md
  AGENTS.md
```

Preserve existing useful work. Do not delete files without inspecting them.

---

## 5. Development Method

Work in strict stages.

For each stage:

1. Inspect the existing repository.
2. Complete only the current stage tasks.
3. Run the required checks.
4. Produce a stage gate report.
5. Continue automatically only if the stage passes.
6. Stop immediately if any required gate fails.
7. Do not hide failures.
8. Do not skip checks.
9. Do not claim success unless commands were actually run.
10. Do not introduce production-write automation.

---

## 6. Universal Checks After Every Stage

Run all applicable checks.

### Git State

```bash
git status --short || true
```

### Backend Checks

Run if backend exists:

```bash
cd backend
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

### Frontend Checks

Run if frontend exists:

```bash
cd frontend
npm install
npm run typecheck || npm run tsc -- --noEmit
npm run lint
npm run build
```

### Docker Checks

Run if Docker Compose exists:

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

### Health Checks

Run if services are expected to be live:

```bash
curl -f http://localhost:8000/api/health/
curl -f http://localhost:5173/
```

---

## 7. Required Stage Gate Report Format

After every stage, output:

```markdown
## Stage X Gate Report

### Status
PASS / FAIL

### Completed Work
- ...

### Commands Run
```bash
...
```

### Results
- Backend checks: PASS/FAIL/N/A
- Frontend checks: PASS/FAIL/N/A
- Docker checks: PASS/FAIL/N/A
- API checks: PASS/FAIL/N/A
- Safety scan: PASS/FAIL/N/A

### Files Changed
- ...

### Notes
- ...

### Next Step
Continuing to Stage X+1 because all gates passed.
```

If failed:

```markdown
## Stage X Gate Report

### Status
FAIL

### Failed Gate
...

### Failed Command
```bash
...
```

### Error Summary
...

### Likely Cause
...

### Files Changed Before Failure
- ...

### Recommended Fix
...

### Next Step
Stopped. Do not continue until this failure is fixed.
```

---

## 8. Core Data Model Requirements

Implement these models unless they already exist correctly:

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

Important relationships:

- AppProfile has many DailyMetric rows.
- AppProfile has many ReviewItem rows.
- AppProfile has many Recommendation rows.
- GrowthReport can create many Recommendations.
- Recommendation can have zero or more ManualActionLog rows.
- Experiment can be linked to recommendations later.

Recommendation statuses must never trigger external API writes.

---

## 9. API Requirements

Use base path:

```text
/api/v1/
```

Required endpoints:

```http
GET    /api/v1/apps/
POST   /api/v1/apps/
GET    /api/v1/apps/{id}/
PATCH  /api/v1/apps/{id}/
DELETE /api/v1/apps/{id}/

GET    /api/v1/daily-metrics/?app={id}&start=YYYY-MM-DD&end=YYYY-MM-DD
POST   /api/v1/daily-metrics/
PATCH  /api/v1/daily-metrics/{id}/
DELETE /api/v1/daily-metrics/{id}/

POST   /api/v1/imports/daily-metrics/
POST   /api/v1/imports/reviews/
POST   /api/v1/imports/android-vitals/
POST   /api/v1/imports/ads/
GET    /api/v1/import-batches/

GET    /api/v1/reviews/?app={id}
POST   /api/v1/reviews/
PATCH  /api/v1/reviews/{id}/
POST   /api/v1/reviews/analyze/?app={id}
GET    /api/v1/review-themes/?app={id}

GET    /api/v1/listing-snapshots/?app={id}
POST   /api/v1/listing-snapshots/
PATCH  /api/v1/listing-snapshots/{id}/
POST   /api/v1/listing-advisor/generate/?app={id}

GET    /api/v1/growth-reports/?app={id}
POST   /api/v1/growth-reports/generate/
GET    /api/v1/growth-reports/{id}/

GET    /api/v1/recommendations/?app={id}&status=suggested
POST   /api/v1/recommendations/
PATCH  /api/v1/recommendations/{id}/
POST   /api/v1/recommendations/{id}/accept/
POST   /api/v1/recommendations/{id}/reject/
POST   /api/v1/recommendations/{id}/mark-implemented/
POST   /api/v1/recommendations/{id}/close/

GET    /api/v1/experiments/?app={id}
POST   /api/v1/experiments/
PATCH  /api/v1/experiments/{id}/
POST   /api/v1/experiments/from-recommendation/{recommendation_id}/

GET    /api/v1/manual-actions/?app={id}
POST   /api/v1/manual-actions/
PATCH  /api/v1/manual-actions/{id}/

GET    /api/v1/dashboard/summary/?app={id}&start=YYYY-MM-DD&end=YYYY-MM-DD
```

Also implement:

```http
GET /api/health/
```

---

## 10. Frontend Screen Requirements

Primary sidebar:

1. Dashboard
2. App Profile
3. Data Import
4. Growth Reports
5. Recommendations
6. Reviews
7. Listing Advisor
8. Experiments
9. Action Log
10. Settings

Dashboard must show:

- Selected app
- Date range selector
- KPI cards
- Growth trend chart
- Bottleneck card
- Top recommendations
- Recent manual actions
- Data freshness warnings

KPI cards:

- installs
- visitors
- conversion rate
- D1 retention
- D7 retention
- average rating
- crash rate
- ad spend
- CPI

Each screen must handle:

- loading state
- empty state
- error state
- small viewport behavior

Do not add forbidden automation buttons.

---

## 11. AI and Diagnosis Requirements

### Diagnosis Engine

Create deterministic rule-based diagnosis before AI.

The diagnosis engine must detect:

- insufficient data
- discovery problem
- store conversion problem
- retention/onboarding problem
- quality/stability problem
- review/theme problem
- ads efficiency problem
- visibility problem
- expectation mismatch

Output shape:

```json
{
  "label": "store_conversion_problem",
  "display_name": "Store conversion problem",
  "evidence": [
    "Store visitors are present but listing conversion is low."
  ],
  "confidence_score": 0.72,
  "recommended_human_action": "Improve screenshot captions and short description clarity.",
  "watch_metric": "listing_conversion_rate"
}
```

### AI Service Layer

Create:

- BaseAIProvider
- MockAIProvider
- AIServiceRouter
- PromptBuilder
- PolicySafetyService
- GrowthAnalysisService
- ReviewAnalysisService
- ListingAdvisorService
- ExperimentPlannerService
- AdsAdvisorService

MVP must work with:

```env
AI_PROVIDER=mock
```

Do not require OpenAI, Gemini, or any external AI key for MVP.

### Recommendation Format

Every recommendation must follow this structure:

```json
{
  "category": "store_listing | product_quality | retention | reviews | ads | experiment",
  "title": "Clear short title",
  "diagnosis": "What seems wrong",
  "evidence": ["Metric or review signal"],
  "suggested_human_action": "Exact action the developer should perform manually",
  "copyable_text": "Optional draft text/caption/reply",
  "do_not_do_yet": "Unsafe or premature action to avoid",
  "expected_impact": "What may improve",
  "watch_metric": "Metric to monitor",
  "risk_level": "low | medium | high",
  "effort_level": "low | medium | high",
  "confidence_score": 0.0
}
```

### Policy Safety Rules

Block or warn against:

- fake installs
- fake reviews
- incentivized reviews
- keyword stuffing
- competitor trademark misuse
- “best”, “#1”, “top rated” without evidence
- “no ads” if ads exist
- “fully offline” if meaningful features require internet
- misleading screenshots
- exaggerated performance claims
- aggressive spending when retention is weak
- daily random listing changes without experiment tracking

---

## 12. CSV Import Requirements

Templates must exist in:

```text
data/templates/
```

Required files:

- daily_metrics.csv
- reviews.csv
- android_vitals.csv
- ads.csv
- country_metrics.csv
- listing_snapshot.csv

Daily metrics header:

```csv
app_package,date,installs,uninstalls,store_visitors,listing_conversion_rate,active_users,day_1_retention,day_7_retention,average_session_length,game_starts,retry_count,daily_challenge_opens,daily_challenge_completions,premium_clicks,premium_purchases,notes
```

Reviews header:

```csv
app_package,date,rating,reviewer_name,review_text,device,app_version,language
```

Android vitals header:

```csv
app_package,date,crash_rate,anr_rate,slow_rendering_rate,excessive_wakeups,affected_devices_json,notes
```

Ads header:

```csv
app_package,date,campaign_name,country_code,spend,impressions,clicks,installs,cpi,conversions,retention_d1,retention_d7,notes
```

Every import must:

- create a DataImportBatch
- validate required columns
- match app by app_package
- validate dates
- validate numeric fields
- collect row-level errors
- return clear error summary
- avoid silent partial failure
- link imported rows to import batch

---

## 13. Seed Data Requirement

Create a management command:

```bash
python manage.py seed_arcade_app
```

It must be idempotent.

It must create or update this app:

```json
{
  "name": "Offline Mini Arcade",
  "package_name": "com.example.offlineminiarcade",
  "play_store_url": "https://play.google.com/store/apps/details?id=com.example.offlineminiarcade",
  "category": "Arcade",
  "app_type": "Game",
  "primary_positioning": "Lightweight offline-first mini arcade with Pulse Orbit, Lane Drift, and Stack Drop. Built for quick sessions and low-end Android devices.",
  "target_countries": "Pakistan, India, Philippines, Indonesia, United States, United Kingdom",
  "monetization_model": "Free / non-aggressive monetization",
  "current_version": "1.0.0"
}
```

---

## 14. Stage Plan and Gates

### Stage 1 — Repository Foundation

Build:

- Docker Compose
- Django backend
- Vite React frontend
- PostgreSQL
- Redis
- Celery
- `.env.example`
- README
- Health endpoint

Gate:

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
curl -f http://localhost:8000/api/health/
curl -f http://localhost:5173/
```

Pass only if backend, frontend, PostgreSQL, Redis, and Celery all start.

---

### Stage 2 — Core Backend Models

Build:

- all core models
- serializers
- viewsets
- routers
- admin registration

Gate:

```bash
cd backend
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py test
```

Smoke:

```bash
curl -f http://localhost:8000/api/v1/apps/
curl -f http://localhost:8000/api/v1/daily-metrics/
curl -f http://localhost:8000/api/v1/reviews/
curl -f http://localhost:8000/api/v1/recommendations/
```

---

### Stage 3 — Seed Data and CSV Templates

Build:

- `seed_arcade_app`
- CSV templates

Gate:

```bash
cd backend
python manage.py seed_arcade_app
python manage.py seed_arcade_app
python manage.py shell -c "from apps.growth.models import AppProfile; print(AppProfile.objects.filter(name='Offline Mini Arcade').count())"
python manage.py test
```

Template checks:

```bash
test -f data/templates/daily_metrics.csv
test -f data/templates/reviews.csv
test -f data/templates/android_vitals.csv
test -f data/templates/ads.csv
test -f data/templates/country_metrics.csv
test -f data/templates/listing_snapshot.csv
```

---

### Stage 4 — Manual Data Entry and CSV Import

Build:

- CSV imports
- import batch tracking
- validation errors
- manual create/edit endpoints

Gate:

```bash
cd backend
python manage.py check
python manage.py test
```

Smoke:

```bash
curl -f -X POST http://localhost:8000/api/v1/imports/daily-metrics/ \
  -F "file=@../data/templates/daily_metrics.csv"

curl -f -X POST http://localhost:8000/api/v1/imports/reviews/ \
  -F "file=@../data/templates/reviews.csv"

curl -f http://localhost:8000/api/v1/import-batches/
curl -f http://localhost:8000/api/v1/daily-metrics/
curl -f http://localhost:8000/api/v1/reviews/
```

Bad CSV test:

```bash
printf "wrong,columns\n1,2\n" > /tmp/bad_import.csv
curl -s -X POST http://localhost:8000/api/v1/imports/daily-metrics/ \
  -F "file=@/tmp/bad_import.csv"
```

Pass only if bad CSV returns a clear validation error.

---

### Stage 5 — Dashboard API and Frontend Shell

Build:

- dashboard summary endpoint
- frontend sidebar
- dashboard KPI cards
- trend chart
- freshness warnings

Gate:

```bash
cd backend
python manage.py test
curl -f "http://localhost:8000/api/v1/dashboard/summary/?app=1&start=2026-06-01&end=2026-06-21"
```

Frontend:

```bash
cd frontend
npm run typecheck || npm run tsc -- --noEmit
npm run lint
npm run build
curl -f http://localhost:5173/
```

---

### Stage 6 — Rule-Based Diagnosis Engine

Build:

- deterministic diagnosis service
- evidence extraction
- confidence score
- watch metric
- tests for all diagnosis categories

Gate:

```bash
cd backend
python manage.py test
python manage.py shell -c "from apps.reports.services.diagnosis import DiagnosisService; print('diagnosis service import ok')"
curl -f "http://localhost:8000/api/v1/dashboard/summary/?app=1&start=2026-06-01&end=2026-06-21"
```

Pass only if diagnosis does not depend on AI.

---

### Stage 7 — AI Service Layer With Mock Provider

Build:

- BaseAIProvider
- MockAIProvider
- AIServiceRouter
- PromptBuilder
- PolicySafetyService
- analysis services

Gate:

```bash
cd backend
python manage.py test
python manage.py shell -c "from apps.ai.providers.mock import MockAIProvider; print(MockAIProvider().generate('test')[:20])"
grep -n "AI_PROVIDER" ../.env.example
```

Pass only if MVP works with `AI_PROVIDER=mock` and no external key.

---

### Stage 8 — Growth Reports and Recommendation Queue

Build:

- report generation
- recommendation generation
- recommendation status transitions
- markdown export
- audit events

Gate:

```bash
cd backend
python manage.py test
curl -f -X POST http://localhost:8000/api/v1/growth-reports/generate/ \
  -H "Content-Type: application/json" \
  -d '{"app":1,"period_start":"2026-06-01","period_end":"2026-06-21","report_type":"weekly"}'

curl -f "http://localhost:8000/api/v1/growth-reports/?app=1"
curl -f "http://localhost:8000/api/v1/recommendations/?app=1"
```

Status smoke:

```bash
curl -f -X POST http://localhost:8000/api/v1/recommendations/1/accept/
curl -f -X POST http://localhost:8000/api/v1/recommendations/1/mark-implemented/
curl -f -X POST http://localhost:8000/api/v1/recommendations/1/close/
```

Pass only if status transitions do not call external systems.

---

### Stage 9 — Review Analyzer

Build:

- review classification
- review themes
- praise themes
- repeated complaints
- copyable manual reply drafts
- recommendations from themes

Gate:

```bash
cd backend
python manage.py test
curl -f "http://localhost:8000/api/v1/reviews/?app=1"
curl -f -X POST "http://localhost:8000/api/v1/reviews/analyze/?app=1"
curl -f "http://localhost:8000/api/v1/review-themes/?app=1"
```

Pass only if no automatic reply sending exists.

---

### Stage 10 — Listing Advisor and Experiment Planner

Build:

- listing snapshots
- listing advisor
- safe copyable suggestions
- experiment CRUD
- recommendation-to-experiment conversion

Gate:

```bash
cd backend
python manage.py test
curl -f "http://localhost:8000/api/v1/listing-snapshots/?app=1"
curl -f -X POST "http://localhost:8000/api/v1/listing-advisor/generate/?app=1"
curl -f "http://localhost:8000/api/v1/experiments/?app=1"
```

Create experiment smoke:

```bash
curl -f -X POST http://localhost:8000/api/v1/experiments/ \
  -H "Content-Type: application/json" \
  -d '{"app":1,"name":"Screenshot caption clarity test","hypothesis":"Clearer screenshot captions improve listing conversion","area":"store_listing","variant_a":"Current captions","variant_b":"Offline-first quick games captions","primary_metric":"listing_conversion_rate","minimum_duration_days":14,"success_rule":"Conversion improves without worse retention","failure_rule":"No improvement after 14 days","status":"planned"}'
```

Pass only if no Play Console publishing/upload/edit feature exists.

---

### Stage 11 — Manual Action Log and Outcome Tracker

Build:

- manual action CRUD
- recommendation linking
- before/after text
- expected metric
- follow-up date
- outcome notes
- simple outcome comparison

Gate:

```bash
cd backend
python manage.py test
curl -f "http://localhost:8000/api/v1/manual-actions/?app=1"

curl -f -X POST http://localhost:8000/api/v1/manual-actions/ \
  -H "Content-Type: application/json" \
  -d '{"app":1,"action_date":"2026-06-22","action_type":"listing_text_change","title":"Updated short description manually","description":"Changed Play Store short description outside the system","changed_location":"Play Console","before_text":"Old text","after_text":"3 quick arcade games that work offline.","expected_metric":"listing_conversion_rate"}'
```

Pass only if action log does not trigger external API calls.

---

### Stage 12 — Internal Validation and Deployment Readiness

Build:

- internal validation docs
- deployment docs
- backup/restore docs
- release checklist
- future integration guardrail

Required docs:

```text
docs/DEPLOYMENT.md
docs/BACKUP_RESTORE.md
docs/RELEASE_CHECKLIST.md
```

Final full checks:

```bash
cd backend
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

```bash
cd frontend
npm run typecheck || npm run tsc -- --noEmit
npm run lint
npm run build
```

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
curl -f http://localhost:8000/api/health/
curl -f http://localhost:5173/
```

Final API smoke:

```bash
curl -f http://localhost:8000/api/v1/apps/
curl -f http://localhost:8000/api/v1/import-batches/
curl -f "http://localhost:8000/api/v1/dashboard/summary/?app=1&start=2026-06-01&end=2026-06-21"
curl -f "http://localhost:8000/api/v1/growth-reports/?app=1"
curl -f "http://localhost:8000/api/v1/recommendations/?app=1"
curl -f "http://localhost:8000/api/v1/reviews/?app=1"
curl -f "http://localhost:8000/api/v1/review-themes/?app=1"
curl -f "http://localhost:8000/api/v1/listing-snapshots/?app=1"
curl -f "http://localhost:8000/api/v1/experiments/?app=1"
curl -f "http://localhost:8000/api/v1/manual-actions/?app=1"
```

Pass only if full stack runs and no production-write automation exists.

---

## 15. Deployment Guidance

Deployment target may later include VPS routing through Caddy at:

```text
play.vexel.pk
```

When preparing Caddy docs or deployment scripts:

- Do not overwrite existing Caddy config blindly.
- Inspect the existing Caddyfile first.
- Preserve all existing routes.
- Add only the PlayGrowth route.
- Validate Caddy config before reload.
- Reload Caddy only after validation.
- Never store sudo passwords, server secrets, API keys, or tokens in the repository.

Example Caddy block for documentation only:

```caddyfile
play.vexel.pk {
    reverse_proxy 127.0.0.1:5173
}
```

Adjust the target port according to the final production service design.

---

## 16. Future Integrations Guardrail

Do not start with Google integrations.

Manual-data MVP comes first.

Future integrations must be read-only unless a later explicit product decision changes this.

Suggested future order:

1. Google Play reports import
2. Play reviews read
3. Android vitals read
4. Firebase/GA4 read
5. Google Ads read

Even for read-only integrations:

- Keep credentials out of Git.
- Use least privilege.
- Log sync jobs.
- Show data freshness.
- Preserve manual CSV fallback.
- Never let integration complexity block the manual MVP.

---

## 17. Final MVP Acceptance Criteria

The MVP is acceptable only when:

- Docker Compose starts.
- Backend health endpoint works.
- Frontend loads.
- Seed app can be created.
- App profile is visible.
- Daily metrics can be added/imported.
- Reviews can be added/imported.
- Android vitals and ads summary can be imported or manually entered.
- Dashboard shows KPI cards.
- Rule diagnosis generates a bottleneck.
- Growth report can be generated using mock AI.
- Recommendations can be generated and status-tracked.
- Reviews can be analyzed into themes.
- Listing suggestions can be generated.
- Experiments can be created.
- Manual actions can be logged.
- Outcomes can be reviewed.
- Audit logs record important generation/status events.
- Deployment docs exist.
- Backup/restore docs exist.
- Release checklist exists.
- No external production-write automation exists.
- UI contains no forbidden automation buttons.
- Tests pass.

---

## 18. Final Agent Behavior

Be careful, staged, and evidence-driven.

Do not over-engineer.

Do not add hidden automation.

Do not skip tests.

Do not continue after a failed gate.

Do not claim success unless verified by commands.

Prefer a stable manual-first product over a risky autonomous system.

The final product should help the developer answer:

- Is my app discoverable?
- Is my listing converting?
- Are users retaining?
- Are crashes or ANRs hurting trust?
- Are reviews revealing repeated product issues?
- Are ads worth testing or should I fix listing/product first?
- What exact manual action should I take next?
- Did my last manual change help or hurt?
