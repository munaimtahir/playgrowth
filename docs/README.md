# PlayGrowth Copilot — AI Dev Pack v2

## Updated Project Identity

**PlayGrowth Copilot** is an AI-assisted growth analyst for Android app developers.

It tracks growth signals, explains what they mean, and suggests exact next steps. It does **not** directly change Play Console listings, Google Ads campaigns, screenshots, app titles, budgets, releases, or production configuration.

## One-line Summary

PlayGrowth Copilot helps Android developers understand growth problems and decide what to do next using manual/imported app data, review analysis, store-listing advice, experiment planning, and an action/outcome log.

## Core Product Shift in v2

The original pack described an approval-based automation system. This version changes the foundation:

- AI can analyze data.
- AI can diagnose bottlenecks.
- AI can draft text and ideas.
- AI can suggest exact human actions.
- AI can help track what the developer manually changed.
- AI must not execute high-risk external changes.

The product should behave like a careful growth consultant, not a growth bot.

## Initial Internal App

The first supported app is an offline-first mini arcade game with three games:

1. Pulse Orbit
2. Lane Drift
3. Stack Drop

Positioning to preserve:

- lightweight
- offline-first
- quick arcade sessions
- low-end Android friendly
- no aggressive monetization
- honest Play Store listing
- no fake growth tactics
- no keyword stuffing
- no fake reviews
- no fake installs

## MVP-0 Goal

Build a practical manual-data MVP before Google API integrations:

1. App profile
2. Manual metric entry and CSV imports
3. Growth dashboard
4. Daily/weekly AI growth report
5. Bottleneck diagnosis
6. Recommendation queue
7. Review analyzer
8. Store listing advisor
9. Experiment planner
10. Manual action log
11. Outcome tracker
12. Audit log

## Recommended Repository Name

`playgrowth-copilot`

## Stack

- Django + Django REST Framework
- PostgreSQL
- Celery + Redis
- Docker Compose
- Vite React + TypeScript
- Tailwind CSS
- Recharts
- Abstract AI service layer for OpenAI/Gemini/local providers later

## Safe Operating Principle

> PlayGrowth Copilot recommends. The developer decides and implements.
