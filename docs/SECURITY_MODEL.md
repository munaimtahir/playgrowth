# Security Model

## Hard constraints

- No public PostgreSQL port
- No public Redis port
- No Play Console write automation
- No Google Ads write automation
- No direct publishing of app metadata
- No secret committed to Git
- No fake reviews or fake installs
- No misleading claims or keyword stuffing

## Operating principle

The software suggests safe manual actions. The developer manually implements changes in Play Console, ads tools, the app codebase, or the store listing.

## Data handling

- CSV imports are local and explicit
- Manual action logs record human changes and results
- Audit logs capture app-side events
- The mock AI provider is the default and requires no API key

## Production exposure

- Caddy is the only public entry point
- Backend listens only on localhost via Docker publish rules
- Frontend listens only on localhost via Docker publish rules
- Database and Redis stay on the internal Docker network

## Practical checks

- Validate Caddy before reload
- Keep `.env.production` out of Git
- Run `collectstatic` after deploy
- Run migrations as a deploy step, not in an endless loop
