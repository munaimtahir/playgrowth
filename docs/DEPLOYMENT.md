# Deployment

## App

- Project path: `/home/munaim/srv/apps/playgrowth-copilot`
- Domain: `play.vexel.pk`
- Frontend container port: `127.0.0.1:3057`
- Backend container port: `127.0.0.1:8057`

## Files

- Docker Compose: `docker-compose.prod.yml`
- Backend Dockerfile: `backend/Dockerfile`
- Frontend Dockerfile: `frontend/Dockerfile`
- Frontend nginx config: `frontend/nginx.conf`
- Caddy source: `/home/munaim/srv/proxy/caddy/Caddyfile`
- Caddy active config: `/etc/caddy/Caddyfile`

## Environment

- Create `/home/munaim/srv/apps/playgrowth-copilot/.env.production`
- Do not commit `.env.production`
- Use strong generated secrets, for example:

```bash
openssl rand -hex 32
```

## Recommended `.env.production`

```env
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=play.vexel.pk,localhost,127.0.0.1,backend
CSRF_TRUSTED_ORIGINS=https://play.vexel.pk
CORS_ALLOWED_ORIGINS=https://play.vexel.pk
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
POSTGRES_DB=playgrowth
POSTGRES_USER=playgrowth
POSTGRES_PASSWORD=...
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
AI_PROVIDER=mock
VITE_API_BASE_URL=https://play.vexel.pk/api/v1
```

## Bring up

```bash
cd /home/munaim/srv/apps/playgrowth-copilot
docker compose -f docker-compose.prod.yml config
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

## Backend deploy steps

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py check
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml exec backend python manage.py test
docker compose -f docker-compose.prod.yml exec backend python manage.py seed_demo
```

## Health checks

```bash
curl -I http://127.0.0.1:3057/
curl -s http://127.0.0.1:8057/api/health/
curl -s http://127.0.0.1:8057/api/v1/
```

After Caddy reload:

```bash
curl -I https://play.vexel.pk/
curl -s https://play.vexel.pk/api/health/
```

## Caddy backup and reload

Backup command:

```bash
timestamp="$(date +%Y%m%d_%H%M%S)"
cp /home/munaim/srv/proxy/caddy/Caddyfile "/home/munaim/srv/proxy/caddy/Caddyfile.bak.$timestamp" 2>/dev/null || true
sudo cp /etc/caddy/Caddyfile "/etc/caddy/Caddyfile.bak.$timestamp" 2>/dev/null || true
sudo cp /etc/caddyfile "/etc/caddyfile.bak.$timestamp" 2>/dev/null || true
```

Reload:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

## Rollback

App rollback:

```bash
cd /home/munaim/srv/apps/playgrowth-copilot
docker compose -f docker-compose.prod.yml down
```

Caddy rollback:

```bash
sudo cp <backup-file> /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```
