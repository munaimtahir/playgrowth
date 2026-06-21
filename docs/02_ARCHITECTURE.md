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
