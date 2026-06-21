# PlayGrowth Copilot

AI-assisted growth analyst for Android app developers.

PlayGrowth Copilot tracks growth metrics, diagnoses bottlenecks, generates safe recommendations, drafts copyable listing/review/experiment ideas, and logs what the developer manually changes. It does **not** directly edit Play Console, Google Ads, screenshots, app titles, budgets, reviews, or production releases.

## MVP-0

Manual-data first:

- App profile
- Manual/CSV metrics import
- Growth dashboard
- Daily/weekly growth report
- Bottleneck diagnosis
- Recommendation queue
- Review analyzer
- Listing advisor
- Experiment planner
- Manual action log
- Audit log

## Tech Stack

- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Worker: Celery + Redis
- Frontend: Vite React + TypeScript
- UI: Tailwind CSS + Recharts
- AI: provider abstraction with Mock provider by default

## Start Locally

```bash
cp .env.example .env
docker compose up --build
```

Development checks:

```bash
cd backend
python manage.py check
python manage.py test

cd ../frontend
npm install
npm run typecheck
npm run lint
npm run build
```

Then open:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/v1/
- Health: http://localhost:8000/api/health/

## Seed Demo Data

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_arcade_app
```

## Safety Rule

The copilot recommends. The developer decides and implements manually.

No external production write automation is included in this scaffold.
