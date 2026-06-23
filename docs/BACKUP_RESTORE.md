# Backup and Restore

## Backup PostgreSQL

Run this command inside the VPS, ideally scheduled daily via cron:

```bash
docker compose exec db pg_dump -U playgrowth playgrowth > backup_$(date +%F).sql
```

## Restore PostgreSQL

```bash
cat backup_YYYY-MM-DD.sql | docker compose exec -T db psql -U playgrowth playgrowth
```
