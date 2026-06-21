# PlayGrowth Copilot — Combined AI Dev Pack v2


---


# README.md

# PlayGrowth Copilot — AI Dev Pack v2

## Updated Project Identity

**PlayGrowth Copilot** is an AI-assisted growth analyst for Android app developers.

It tracks growth signals, explains what they mean, and suggests exact next steps. It does **not** directly change Play Console listings, Google Ads campaigns, screenshots, app titles, budgets, releases, or production configuration.

## One-line Summary

PlayGrowth Copilot helps Android developers understand growth problems and decide what to do next using manual/imported app data, review analysis, store-listing advice, experiment planning, and an action/outcome log.

## Core Product Shift in v2

The original pack described an approval-based automation system. This version changes the foundation:

- AI can analyze data.
- AI can diagnose bottlenecks.
- AI can draft text and ideas.
- AI can suggest exact human actions.
- AI can help track what the developer manually changed.
- AI must not execute high-risk external changes.

The product should behave like a careful growth consultant, not a growth bot.

## Initial Internal App

The first supported app is an offline-first mini arcade game with three games:

1. Pulse Orbit
2. Lane Drift
3. Stack Drop

Positioning to preserve:

- lightweight
- offline-first
- quick arcade sessions
- low-end Android friendly
- no aggressive monetization
- honest Play Store listing
- no fake growth tactics
- no keyword stuffing
- no fake reviews
- no fake installs

## MVP-0 Goal

Build a practical manual-data MVP before Google API integrations:

1. App profile
2. Manual metric entry and CSV imports
3. Growth dashboard
4. Daily/weekly AI growth report
5. Bottleneck diagnosis
6. Recommendation queue
7. Review analyzer
8. Store listing advisor
9. Experiment planner
10. Manual action log
11. Outcome tracker
12. Audit log

## Recommended Repository Name

`playgrowth-copilot`

## Stack

- Django + Django REST Framework
- PostgreSQL
- Celery + Redis
- Docker Compose
- Vite React + TypeScript
- Tailwind CSS
- Recharts
- Abstract AI service layer for OpenAI/Gemini/local providers later

## Safe Operating Principle

> PlayGrowth Copilot recommends. The developer decides and implements.


---


# 00_EXECUTIVE_SUMMARY.md

# Executive Summary — PlayGrowth Copilot v2

## What We Are Building

PlayGrowth Copilot is a private growth command center for Android app developers. It brings app growth data, reviews, store listing notes, crash/vitals summaries, ads summaries, and experiment history into one dashboard, then uses AI and rules to explain what is happening and what the developer should do next.

## What Changed from the Earlier Concept

The product is no longer framed as an automation system that prepares or performs external changes. The new concept is a **controlled recommendation and tracking system**.

### Old Direction

- AI prepares changes.
- Approval workflow is central.
- Future integrations may write to Play Console or Ads.
- The product could become semi-autonomous.

### New Direction

- AI analyzes, diagnoses, and suggests.
- The developer manually implements changes outside the system.
- The system records what was suggested, what the developer did, and whether metrics improved.
- No Play Console writes, screenshot uploads, ad budget changes, campaign launches, or production publishing from the MVP.

## Product Role

The product is best understood as an:

- ASO analyst
- growth analyst
- product-quality analyst
- review analyst
- ads advisor
- experiment planner
- decision log

It is not an autonomous marketing bot.

## MVP Definition

MVP-0 should work without external Google API integrations. It should support manual data input and CSV imports so the product logic can be validated before adding integrations.

## Primary Jobs-to-be-Done

1. Tell me whether my app has a visibility, conversion, retention, quality, or ads problem.
2. Tell me what exact change I should make next.
3. Help me improve my Play Store listing without misleading users.
4. Extract useful themes from Play reviews.
5. Help me plan experiments I can manually run.
6. Track whether my manual changes improved outcomes.

## Non-negotiable Constraints

- No fake installs.
- No fake reviews.
- No keyword stuffing.
- No competitor-name misuse.
- No exaggerated claims.
- No auto-publishing.
- No automatic ad-budget increase.
- No direct production writes in MVP.
- Every recommendation must include evidence, confidence, effort, risk, and a suggested next action.


---


# 01_PRODUCT_REQUIREMENTS.md

# Product Requirements Document — PlayGrowth Copilot v2

## 1. Product Vision

PlayGrowth Copilot helps Android developers understand why their app is or is not growing, then gives practical, evidence-based recommendations the developer can manually implement.

The product should make a solo developer feel like they have a disciplined growth analyst reviewing their app every day.

## 2. Problem Statement

Android developers often launch an app and then struggle to answer basic growth questions:

- Are people finding the store listing?
- Are visitors converting into installs?
- Are installs coming from the right countries?
- Are users retaining after installation?
- Are crashes or ANRs hurting user trust?
- Are reviews exposing repeated product problems?
- Are ads bringing quality users or wasting money?
- Is the Play Store listing honest, clear, and convincing?
- Which change should be tested next?
- Did the last manual change help or harm growth?

Most developers have fragmented data across Play Console, Firebase/GA4, Android vitals, Google Ads, notes, screenshots, and reviews. They need diagnosis and prioritization more than automation.

## 3. Target Users

### Primary Users

- Indie Android developers
- Solo game developers
- Small studios
- Early-stage app founders
- Developers launching their first Google Play app

### Initial Internal User

The first internal app is an offline-first mini arcade game containing:

1. Pulse Orbit
2. Lane Drift
3. Stack Drop

The game should be positioned honestly as lightweight, offline-first, quick-session, low-end Android friendly, and non-aggressively monetized.

## 4. Product Principles

### The System Must Be

- Evidence-driven
- Human-controlled
- Recommendation-first
- Simple enough for a solo developer
- Honest about confidence and limitations
- Conservative with store and ads advice
- Focused on quality growth, not vanity numbers
- Useful before API integrations exist

### The System Must Avoid

- Fake reviews
- Fake installs
- Keyword stuffing
- Misleading claims
- Competitor keyword abuse
- Aggressive monetization pressure
- Daily chaotic listing changes
- Unjustified ad spending
- Automated production changes

## 5. MVP-0 Goal

Build a working local/manual-data growth copilot that can:

1. Store app profile and positioning.
2. Accept manual daily metrics and CSV imports.
3. Store Play review excerpts and ratings.
4. Store crash/vitals summaries.
5. Store ads summary metrics.
6. Show a dashboard of growth signals.
7. Generate rule-based bottleneck diagnosis.
8. Generate AI-assisted daily/weekly reports.
9. Create recommendation cards with evidence and next steps.
10. Suggest Play Store listing improvements.
11. Analyze reviews into themes.
12. Build structured experiment plans.
13. Log what the developer manually changed.
14. Track before/after outcomes.
15. Maintain an audit trail of AI outputs and user decisions.

## 6. MVP-0 Scope

### Included

- Single-user or simple admin login
- App profile management
- Manual data entry forms
- CSV import templates
- Dashboard
- Recommendation queue
- Review analyzer
- Listing advisor
- Experiment planner
- Manual action log
- Outcome tracker
- Audit log
- Demo seed data for the arcade game
- AI provider abstraction with a mock provider fallback

### Not Included

- Google Play Console write integration
- Google Ads write integration
- Automatic review replies
- Automatic screenshot generation/upload
- Automatic title/description edits
- Automatic publishing
- Multi-tenant SaaS billing
- Public onboarding
- Autonomous growth execution

## 7. Recommendation Philosophy

A recommendation must answer:

- What is the problem?
- What evidence supports it?
- What exact human action should be taken?
- What should not be done yet?
- How risky is it?
- How much effort is required?
- What metric should be watched afterward?
- When should the decision be reviewed?

## 8. Success Criteria

MVP-0 is successful when it can:

- Import or manually enter 7–30 days of app data.
- Identify the most likely bottleneck.
- Generate a clear growth report.
- Suggest safe listing improvements.
- Extract review themes.
- Create at least three experiment ideas.
- Let the developer mark recommendations as accepted, rejected, implemented, or monitoring.
- Track manual actions against later outcomes.
- Run locally through Docker Compose.

## 9. First Internal Success Target

For the arcade game, the product should help answer:

- Is the Play Store listing converting?
- Are screenshots clearly explaining Pulse Orbit, Lane Drift, and Stack Drop?
- Is offline-first positioning visible enough?
- Is the app lightweight positioning believable?
- Are users complaining about controls, crashes, difficulty, boredom, or confusion?
- Should the next action be listing improvement, product fix, review response, or ad testing?


---


# 02_ARCHITECTURE.md

# Architecture Plan — PlayGrowth Copilot v2

## 1. Architecture Goal

Build a simple, reliable, local-first MVP that can run through Docker Compose and support manual data workflows before external API integrations.

The architecture should keep data ingestion, diagnosis, AI generation, and UI presentation separate.

## 2. Recommended Stack

### Backend

- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- django-cors-headers
- django-filter

### Frontend

- Vite React
- TypeScript
- Tailwind CSS
- Recharts
- React Router

### AI Layer

- Provider abstraction
- Mock provider for local development
- Optional later providers: OpenAI, Gemini, local model service

### Deployment

- Docker Compose
- `.env` file
- Backend container
- Frontend container
- PostgreSQL container
- Redis container
- Celery worker container
- Optional Celery beat container

## 3. High-Level Data Flow

```text
Manual Entry / CSV Import
        ↓
Raw + Normalized App Metrics
        ↓
Rule-Based Diagnosis Engine
        ↓
AI Service Layer
        ↓
Growth Report + Recommendation Cards
        ↓
Developer Manual Action
        ↓
Action Log + Outcome Tracking
```

## 4. Important Design Change

There is no external write/action executor in MVP-0.

Do not build:

- Play Store edit executor
- Ads budget executor
- Screenshot upload executor
- Publishing executor
- Review reply sender

Instead build:

- Suggestion generator
- Human action checklist
- Copyable drafts
- Before/after notes
- Outcome tracking

## 5. Backend Modules

### App Management

Stores app profile, package name, Play Store URL, positioning, monetization, countries, and current listing snapshot.

### Manual Data Ingestion

Supports manual entry and CSV imports for:

- Daily metrics
- Country metrics
- Reviews
- Android vitals
- Ads summaries
- Listing snapshots

### Diagnosis Engine

A deterministic rule-based layer that detects likely bottlenecks. This protects the product from relying blindly on AI.

### AI Insight Layer

Uses structured prompts and provider abstraction to generate:

- Growth reports
- Recommendation explanations
- Listing suggestions
- Review summaries
- Experiment plans

### Recommendation Queue

Stores recommendations with status and evidence. It is not an approval queue for automatic external execution. It is a work queue for the developer.

### Action Log

The developer records what was manually changed outside the system.

Examples:

- Changed short description in Play Console.
- Reordered screenshots.
- Added clearer control label in app.
- Reduced first-run difficulty.
- Paused ads in one country.

### Outcome Tracker

Compares metrics before and after manual actions.

### Audit Log

Records generated reports, recommendations, imports, and user status changes.

## 6. Frontend Modules

- Dashboard
- App Profile
- Manual Import
- Growth Reports
- Recommendations
- Review Analyzer
- Listing Advisor
- Experiments
- Action Log
- Settings

## 7. Future Integrations

Future integrations should be read-first:

1. Google Play reports import
2. Play review fetch
3. Android vitals read
4. Firebase/GA4 read
5. Google Ads read

Write APIs should remain out of scope until the decision-support product is mature. Even then, write actions should be optional and disabled by default.

## 8. Security and Privacy

- Store credentials in environment variables only.
- Never commit API keys.
- Log AI prompts and outputs carefully.
- Avoid sending unnecessary user or reviewer personal data to AI providers.
- Use a configurable AI redaction layer later.
- Keep raw imports traceable to an import batch.

## 9. MVP Deployment Target

Local development and VPS-ready Docker Compose:

```bash
docker compose up --build
```

Expected services:

- backend: `http://localhost:8000`
- frontend: `http://localhost:5173`
- PostgreSQL: internal service
- Redis: internal service
- Celery worker: internal service


---


# 03_DATA_MODEL.md

# Data Model — PlayGrowth Copilot v2

## 1. Core Concepts

The data model is designed around five loops:

1. App identity
2. Growth signal tracking
3. Diagnosis and recommendations
4. Manual implementation logging
5. Outcome review

## 2. Models

### AppProfile

Stores the app being tracked.

Fields:

- id
- name
- package_name
- play_store_url
- category
- app_type
- primary_positioning
- target_countries
- monetization_model
- current_version
- notes
- created_at
- updated_at

### DataImportBatch

Tracks manual imports.

Fields:

- id
- app
- import_type
- source_filename
- source_label
- row_count
- status
- error_summary
- created_at

Import types:

- daily_metrics
- country_metrics
- reviews
- android_vitals
- ads
- listing_snapshot

### DailyMetric

One row per app per date.

Fields:

- id
- app
- date
- installs
- uninstalls
- store_visitors
- listing_conversion_rate
- active_users
- day_1_retention
- day_7_retention
- average_session_length
- game_starts
- retry_count
- daily_challenge_opens
- daily_challenge_completions
- premium_clicks
- premium_purchases
- notes
- import_batch
- created_at

### CountryMetric

Fields:

- id
- app
- date
- country_code
- installs
- visitors
- conversion_rate
- retention_d1
- retention_d7
- ad_spend
- cpi
- notes
- import_batch

### StoreListingSnapshot

Stores the listing at a point in time.

Fields:

- id
- app
- snapshot_date
- app_title
- short_description
- full_description
- screenshot_notes
- feature_graphic_notes
- video_notes
- language
- status
- notes
- created_at

Statuses:

- current
- draft
- historical
- proposed

### ReviewItem

Fields:

- id
- app
- review_external_id
- date
- rating
- reviewer_name
- review_text
- device
- app_version
- language
- sentiment
- category
- ai_summary
- suggested_reply
- status
- import_batch
- created_at

Review statuses:

- new
- analyzed
- needs_product_fix
- reply_drafted
- manually_replied
- ignored

### ReviewTheme

Aggregated issue or praise cluster.

Fields:

- id
- app
- date_range_start
- date_range_end
- category
- theme
- count
- severity
- examples_json
- recommendation
- created_at

### AndroidVitalsMetric

Fields:

- id
- app
- date
- crash_rate
- anr_rate
- slow_rendering_rate
- excessive_wakeups
- affected_devices_json
- notes
- import_batch

### AdCampaignMetric

Fields:

- id
- app
- date
- campaign_name
- country_code
- spend
- impressions
- clicks
- installs
- cpi
- conversions
- retention_d1
- retention_d7
- notes
- import_batch

### GrowthReport

AI/rule-generated report.

Fields:

- id
- app
- report_date
- period_start
- period_end
- report_type
- summary
- bottleneck
- evidence_json
- next_actions_json
- confidence_score
- ai_provider
- created_at

Report types:

- daily
- weekly
- custom

### Recommendation

A human action suggestion.

Fields:

- id
- app
- source_report
- date
- category
- title
- diagnosis
- evidence_json
- suggested_human_action
- copyable_text
- do_not_do_yet
- expected_impact
- risk_level
- effort_level
- confidence_score
- status
- watch_metric
- review_after_days
- created_at
- accepted_at
- implemented_at
- closed_at
- result_summary

Statuses:

- suggested
- accepted_to_try
- rejected
- manually_implemented
- monitoring
- successful
- unsuccessful
- closed

Important: these statuses do not trigger external API writes.

### Experiment

Fields:

- id
- app
- name
- hypothesis
- area
- variant_a
- variant_b
- primary_metric
- secondary_metric
- minimum_duration_days
- minimum_sample_size
- success_rule
- failure_rule
- start_date
- end_date
- status
- result
- decision
- created_at

Statuses:

- idea
- planned
- running_manually
- completed
- stopped
- archived

### ManualActionLog

Records what the developer manually changed.

Fields:

- id
- app
- recommendation
- action_date
- action_type
- title
- description
- changed_location
- before_text
- after_text
- expected_metric
- followup_date
- outcome_notes
- created_at

Action types:

- listing_text_change
- screenshot_change
- feature_graphic_change
- app_update
- bug_fix
- control_improvement
- ads_change
- review_response
- experiment_started
- experiment_ended
- other

### AuditLog

Fields:

- id
- app
- actor
- event_type
- object_type
- object_id
- summary
- metadata_json
- created_at

## 3. MVP Relationships

- AppProfile has many DailyMetric rows.
- AppProfile has many ReviewItem rows.
- AppProfile has many Recommendation rows.
- GrowthReport can create many Recommendations.
- Recommendation can have zero or more ManualActionLog rows.
- Experiment can be linked to recommendations later.

## 4. Seed Data for Internal App

Create one AppProfile:

- name: Offline Mini Arcade
- app_type: Game
- category: Arcade
- package_name: placeholder until final package is added
- primary_positioning: Lightweight offline-first mini arcade with Pulse Orbit, Lane Drift, and Stack Drop.
- target_countries: Pakistan, India, Philippines, Indonesia, United States, United Kingdom
- monetization_model: Free / non-aggressive monetization


---


# 04_AI_SERVICES_AND_RULES.md

# AI Services and Decision Rules — PlayGrowth Copilot v2

## 1. AI Role

AI is used for interpretation, drafting, summarization, and structured recommendations.

AI does not execute production changes.

## 2. AI Service Layer

The backend should expose clean service classes:

### GrowthAnalysisService

Purpose:

- Analyze metrics
- Identify likely bottleneck
- Generate daily/weekly report
- Recommend next human actions

Inputs:

- AppProfile
- DailyMetric
- CountryMetric
- AndroidVitalsMetric
- AdCampaignMetric
- ReviewTheme
- StoreListingSnapshot
- ManualActionLog

Outputs:

- GrowthReport
- Recommendation cards

### ReviewAnalysisService

Purpose:

- Classify reviews
- Detect repeated complaints
- Extract praise
- Draft optional manual reply text
- Identify product fixes before marketing pushes

Categories:

- bug/crash
- performance
- controls
- difficulty
- confusion
- ads/monetization
- offline issue
- praise
- feature request
- pricing
- other

### ListingAdvisorService

Purpose:

- Suggest clearer Play Store text
- Draft honest short descriptions
- Draft full description sections
- Suggest screenshot captions
- Suggest feature graphic concepts
- Identify keyword stuffing risk

### ExperimentPlannerService

Purpose:

- Convert a recommendation into a testable manual experiment.

### AdsAdvisorService

Purpose:

- Analyze imported ads metrics
- Warn against spending when conversion/retention/quality is weak
- Suggest manual campaign cleanup or observation plans

### PolicySafetyService

Purpose:

- Reject or flag unsafe suggestions.

## 3. Policy Safety Rules

Block or warn against:

- Fake installs
- Fake reviews
- Incentivized reviews
- Keyword stuffing
- Competitor trademark misuse
- “Best”, “#1”, “top rated” without evidence
- “No ads” if ads exist
- “Fully offline” if meaningful features require internet
- Misleading screenshots
- Exaggerated performance claims
- Aggressive spending when retention is weak
- Daily random listing changes without experiment tracking

## 4. Bottleneck Diagnosis Rules

| Signal | Likely Diagnosis | Recommended Human Action |
|---|---|---|
| Low impressions and low visitors | Discovery problem | Improve ASO structure and metadata clarity |
| Visitors adequate but install conversion low | Store conversion problem | Improve screenshots, short description, value proposition |
| Installs adequate but D1 retention low | Product/onboarding problem | Improve first-run experience and core loop clarity |
| Reviews mention controls repeatedly | UX/control clarity problem | Fix controls before scaling ads |
| Crash/ANR rate high | Quality problem | Fix stability before listing/ads push |
| Ads CPI high and conversion low | Ads/listing mismatch | Pause scale; refine store listing and targeting manually |
| Good retention but low visitors | Visibility problem | Improve organic discovery and consider small manual ad tests |
| High uninstalls | Expectation mismatch or quality issue | Compare listing promise with actual experience |

## 5. Recommendation Format

Every recommendation must include:

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

## 6. Prompting Principles

AI prompts should:

- Include app positioning.
- Include only relevant metric windows.
- Ask for conservative recommendations.
- Require evidence for each claim.
- Require exact next action.
- Require “do not do yet” guidance.
- Reject fake or manipulative growth tactics.
- Prefer fewer prioritized actions over long generic lists.

## 7. Example Recommendation

### Signal

Visitors are present, but conversion rate is weak. Reviews are not yet enough to identify product themes.

### Diagnosis

Store listing value proposition may not be clear enough.

### Human Action

Manually update the first screenshot caption to explain the core value faster:

> “3 quick arcade games. Works offline. Play in short breaks.”

### Do Not Do Yet

Do not increase ad budget until listing conversion improves.

### Watch Metric

Store listing conversion rate over the next 7–14 days.


---


# 05_UI_SCREEN_PLAN.md

# UI Screen Plan — PlayGrowth Copilot v2

## 1. Navigation

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

## 2. Dashboard

Purpose:
Show the current growth state at a glance.

Sections:

- Selected app
- Date range selector
- KPI cards
  - installs
  - visitors
  - conversion rate
  - D1 retention
  - D7 retention
  - average rating
  - crash rate
  - ad spend
  - CPI
- Growth trend chart
- Bottleneck card
- Top recommendations
- Recent manual actions
- Data freshness warnings

## 3. App Profile

Purpose:
Store the app identity and positioning used by the AI.

Fields:

- App name
- Package name
- Play Store URL
- Category
- App type
- Target countries
- Monetization model
- Positioning statement
- Notes

For the initial app, include structured positioning chips:

- Offline-first
- Lightweight
- Quick sessions
- Low-end Android friendly
- 3 mini games
- No aggressive monetization

## 4. Data Import

Purpose:
Support manual-first MVP.

Sections:

- Add daily metric manually
- Upload daily metrics CSV
- Upload reviews CSV
- Upload Android vitals CSV
- Upload ads summary CSV
- Import history
- Download CSV templates

## 5. Growth Reports

Purpose:
Show AI/rule-generated reports.

Report card sections:

- Summary
- Main bottleneck
- Evidence
- What changed since previous period
- What to do next
- What not to do yet
- Confidence

Actions:

- Generate report
- Create recommendations from report
- Export as markdown

## 6. Recommendations

Purpose:
A prioritized work queue for the developer.

Columns or filters:

- Suggested
- Accepted to try
- Manually implemented
- Monitoring
- Successful/Unsuccessful
- Rejected/Closed

Recommendation card:

- Title
- Category
- Evidence
- Suggested human action
- Copyable text
- Do not do yet
- Expected impact
- Watch metric
- Risk
- Effort
- Confidence
- Status buttons
- Create manual action log

## 7. Reviews

Purpose:
Turn reviews into product/growth intelligence.

Sections:

- Rating distribution
- Review list
- AI themes
- Repeated complaints
- Praise themes
- Reply drafts for manual use
- Product fix suggestions

## 8. Listing Advisor

Purpose:
Generate safe, honest listing improvements.

Sections:

- Current listing snapshot
- Short description drafts
- Full description structure
- Screenshot caption ideas
- Feature graphic ideas
- ASO clarity checklist
- Policy safety warnings

Important:
The user copies suggestions manually into Play Console. There is no publish button.

## 9. Experiments

Purpose:
Plan manual experiments.

Experiment fields:

- Hypothesis
- Area
- Variant A
- Variant B
- Primary metric
- Secondary metric
- Minimum duration
- Success rule
- Failure rule
- Status
- Decision

## 10. Action Log

Purpose:
Record what the developer actually changed outside the system.

Examples:

- Changed short description
- Uploaded new screenshot set
- Updated app controls
- Fixed crash
- Paused ad campaign manually
- Started Play Console store listing experiment manually

## 11. Settings

Purpose:
Configure the local product.

Sections:

- AI provider setting
- API base URL
- Data retention preferences
- Safety mode
- Export/backup


---


# 06_API_DESIGN.md

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


---


# 07_IMPLEMENTATION_ROADMAP.md

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


---


# 08_CODING_AGENT_PROMPT.md

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


---


# 09_NEW_CHAT_HANDOFF.md

# New Chat Handoff — PlayGrowth Copilot v2

## Project Name

PlayGrowth Copilot

## Updated Concept

PlayGrowth Copilot is an AI-assisted growth analyst for Android app developers. It tracks growth signals and suggests what the developer should manually do next.

It should not directly implement Play Store, Google Ads, Firebase, review, screenshot, title, budget, or publishing changes.

## Core Principle

> The copilot recommends. The developer decides and implements.

## Initial Internal App

Offline-first mini arcade game with three games:

1. Pulse Orbit
2. Lane Drift
3. Stack Drop

Positioning:

- lightweight
- offline-first
- quick arcade sessions
- low-end Android friendly
- no aggressive monetization
- honest listing
- no fake growth tactics
- no keyword stuffing
- no fake reviews
- no fake installs

## MVP-0

Manual-data first. Do not start with complex Google API integrations.

Build:

- Dashboard
- Manual imports
- Daily/weekly growth report
- Bottleneck diagnosis
- Recommendation queue
- Review analyzer
- Listing advisor
- Experiment planner
- Manual action log
- Outcome tracker
- Audit log

## Stack

- Django + DRF
- PostgreSQL
- Celery + Redis
- Docker Compose
- Vite React + TypeScript
- Tailwind CSS
- Recharts
- Abstract AI provider layer

## Key Product Decision

Remove the automation-first mindset. The MVP is not approval-based automation. It is decision support and manual implementation tracking.

## Repository Name

`playgrowth-copilot`

## First Coding Goal

Create a GitHub-ready scaffold with backend, frontend, Docker Compose, docs, seed data, and CSV templates. The app should run locally and support manual app metrics/review data before any Google API work.


---


# 10_SAMPLE_SEED_DATA.md

# Sample Seed Data — Offline Mini Arcade

## App Profile

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

## Sample Daily Metrics

```csv
date,installs,uninstalls,store_visitors,listing_conversion_rate,active_users,day_1_retention,day_7_retention,average_session_length,game_starts,retry_count,daily_challenge_opens,daily_challenge_completions,premium_clicks,premium_purchases,notes
2026-06-01,4,1,80,5.0,12,20.0,8.0,130,32,18,2,1,0,0,Launch week baseline
2026-06-02,6,1,95,6.3,16,22.0,8.5,145,44,21,3,1,0,0,Slight improvement
2026-06-03,5,2,100,5.0,15,18.0,7.0,125,39,19,3,1,0,0,Conversion still low
```

## Sample Reviews

```csv
date,rating,reviewer_name,review_text,device,app_version,language
2026-06-02,5,User A,"Nice small games and works offline.",TECNO CH6i,1.0.0,en
2026-06-03,3,User B,"Stack game controls feel a little cramped on my phone.",Samsung A10,1.0.0,en
2026-06-04,4,User C,"Good for short breaks. Please add more levels.",Redmi 9A,1.0.0,en
```

## First Expected Diagnosis

If visitors are present but conversion remains low, the system should suggest a store conversion problem rather than an ads push.

## First Expected Recommendations

1. Improve screenshot captions to explain the three games faster.
2. Add clearer offline-first wording in the short description.
3. Avoid increasing ads budget until listing conversion improves.
4. Track conversion for 7–14 days after manual listing update.


---


# 11_CSV_TEMPLATES.md

# CSV Templates

## daily_metrics.csv

```csv
app_package,date,installs,uninstalls,store_visitors,listing_conversion_rate,active_users,day_1_retention,day_7_retention,average_session_length,game_starts,retry_count,daily_challenge_opens,daily_challenge_completions,premium_clicks,premium_purchases,notes
com.example.offlineminiarcade,2026-06-01,4,1,80,5.0,12,20.0,8.0,130,32,18,2,1,0,0,Launch week baseline
```

## reviews.csv

```csv
app_package,date,rating,reviewer_name,review_text,device,app_version,language
com.example.offlineminiarcade,2026-06-02,5,User A,"Nice small games and works offline.",TECNO CH6i,1.0.0,en
```

## android_vitals.csv

```csv
app_package,date,crash_rate,anr_rate,slow_rendering_rate,excessive_wakeups,affected_devices_json,notes
com.example.offlineminiarcade,2026-06-01,0.4,0.1,2.2,0,"[]",No major issue
```

## ads.csv

```csv
app_package,date,campaign_name,country_code,spend,impressions,clicks,installs,cpi,conversions,retention_d1,retention_d7,notes
com.example.offlineminiarcade,2026-06-01,Launch Test,PK,2.5,1200,80,5,0.5,0,20.0,8.0,Small test only
```


---


# 12_FUTURE_READ_ONLY_INTEGRATIONS.md

# Future Read-Only Integration Plan

## Important Rule

Do not start here. Build the manual-data MVP first.

## Integration Philosophy

Future integrations should pull data into PlayGrowth Copilot. They should not directly perform production changes.

## Suggested Order

### 1. Google Play Reports Import

Purpose:

- Store visitors
- Acquisition metrics
- Installs
- Country breakdown
- Conversion data

Approach:

- Prefer report download/import first.
- Later use Cloud Storage reports if needed.

### 2. Google Play Reviews Read

Purpose:

- Fetch reviews
- Analyze themes
- Draft manual replies

No automatic reply sending in MVP.

### 3. Android Vitals Read

Purpose:

- Crash rate
- ANR rate
- Device-specific issues

### 4. Firebase/GA4 Read

Purpose:

- App open
- Game start
- Game end
- Retry tapped
- Daily challenge opened/completed
- Session length
- Retention proxies

### 5. Google Ads Read

Purpose:

- Campaign performance
- Spend
- CPI
- Country performance
- Conversion quality

No budget changes or campaign launches from the product.

## Integration Safety

Even for read-only integrations:

- Keep credentials out of Git.
- Use least privilege.
- Log sync jobs.
- Show data freshness.
- Preserve manual import fallback.
- Never let integration complexity block the manual MVP.
