# PlayGrowth Copilot

PlayGrowth Copilot is an AI-assisted growth analyst for Android app developers.

It tracks growth metrics, diagnoses bottlenecks, drafts safe recommendations, suggests experiments, analyzes reviews, and logs manual actions. It does not directly change Play Console listings, app metadata, ad budgets, production releases, or review responses.

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

## Production deployment

- App path: `/home/munaim/srv/apps/playgrowth-copilot`
- Domain: `play.vexel.pk`
- Frontend port: `127.0.0.1:3057`
- Backend port: `127.0.0.1:8057`
- Caddy source: `/home/munaim/srv/proxy/caddy/Caddyfile`
- Caddy active config: `/etc/caddy/Caddyfile`

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the exact runbook.

## Local / server startup

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml exec backend python manage.py seed_demo
```

## Safety

See [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md) and [docs/AI_SAFETY_RULES.md](docs/AI_SAFETY_RULES.md).
