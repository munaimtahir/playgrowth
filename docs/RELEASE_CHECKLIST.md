# Release Checklist

Before marking an MVP release, ensure:

1. [ ] Safety check script returns no forbidden auto-publish actions.
2. [ ] All backend test pass: `python manage.py test`.
3. [ ] All frontend builds pass: `npm run build`.
4. [ ] AI_PROVIDER defaults to `mock` in `settings.py` or `.env.example`.
5. [ ] Ensure no real Google API credentials or integrations exist yet. (Future integration must be read-only).
