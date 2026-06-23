# Deployment Guide

PlayGrowth Copilot MVP is designed for manual tracking.

## Standard Deployment

1. Provision an Ubuntu VPS.
2. Install Docker and Docker Compose.
3. Clone repository.
4. Copy `.env.example` to `.env` and fill secrets.
5. Bring up services:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
   ```

## Routing with Caddy

If using Caddy for `play.vexel.pk`:

1. Check existing routes: `cat /etc/caddy/Caddyfile`
2. DO NOT blind overwrite. Preserve existing routes.
3. Add:
   ```caddyfile
   play.vexel.pk {
       reverse_proxy 127.0.0.1:5173
   }
   ```
   (Adjust 5173 to your exposed frontend port or routing setup)
4. Validate: `caddy validate --config /etc/caddy/Caddyfile`
5. Reload: `caddy reload --config /etc/caddy/Caddyfile`

## Secrets
Never commit passwords, secrets, or API keys to this repository.
