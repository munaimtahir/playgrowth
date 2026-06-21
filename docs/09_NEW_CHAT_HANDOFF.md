# New Chat Handoff — PlayGrowth Copilot v2

## Project Name

PlayGrowth Copilot

## Updated Concept

PlayGrowth Copilot is an AI-assisted growth analyst for Android app developers. It tracks growth signals and suggests what the developer should manually do next.

It should not directly implement Play Store, Google Ads, Firebase, review, screenshot, title, budget, or publishing changes.

## Core Principle

> The copilot recommends. The developer decides and implements.

## Initial Internal App

Offline-first mini arcade game with three games:

1. Pulse Orbit
2. Lane Drift
3. Stack Drop

Positioning:

- lightweight
- offline-first
- quick arcade sessions
- low-end Android friendly
- no aggressive monetization
- honest listing
- no fake growth tactics
- no keyword stuffing
- no fake reviews
- no fake installs

## MVP-0

Manual-data first. Do not start with complex Google API integrations.

Build:

- Dashboard
- Manual imports
- Daily/weekly growth report
- Bottleneck diagnosis
- Recommendation queue
- Review analyzer
- Listing advisor
- Experiment planner
- Manual action log
- Outcome tracker
- Audit log

## Stack

- Django + DRF
- PostgreSQL
- Celery + Redis
- Docker Compose
- Vite React + TypeScript
- Tailwind CSS
- Recharts
- Abstract AI provider layer

## Key Product Decision

Remove the automation-first mindset. The MVP is not approval-based automation. It is decision support and manual implementation tracking.

## Repository Name

`playgrowth-copilot`

## First Coding Goal

Create a GitHub-ready scaffold with backend, frontend, Docker Compose, docs, seed data, and CSV templates. The app should run locally and support manual app metrics/review data before any Google API work.
