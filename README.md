# PlayGrowth Copilot

AI-assisted growth analyst for Android app developers.

PlayGrowth Copilot tracks growth metrics, diagnoses bottlenecks, drafts safe recommendations, suggests experiments, analyzes reviews, and logs manual actions. It does **not** directly edit Play Console, Google Ads, screenshots, app titles, budgets, reviews, or production releases.

## Core rule

The copilot recommends. The developer decides and implements manually.

## MVP Scope

- App profile
- Daily metrics
- CSV imports
- Dashboard
- Growth reports
- Bottleneck diagnosis
- Recommendation queue
- Review analysis
- Listing advisor drafts
- Experiment planner
- Manual action log
- Audit log

## Repository layout

- `backend/` Django + DRF API, Celery, mock AI provider
- `frontend/` Vite React app built into nginx
- `docs/` deployment, security, safety, and roadmap notes
- `data/templates/` CSV templates

## Local development

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

## Production deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the runbook and [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md) for the safety model.

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml exec backend python manage.py seed_demo
```

## Safety

The copilot recommends. The developer decides and implements manually.

No external production write automation is included in this scaffold.
