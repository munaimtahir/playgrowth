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
