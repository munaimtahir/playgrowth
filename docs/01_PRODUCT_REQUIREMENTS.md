# Product Requirements Document — PlayGrowth Copilot v2

## 1. Product Vision

PlayGrowth Copilot helps Android developers understand why their app is or is not growing, then gives practical, evidence-based recommendations the developer can manually implement.

The product should make a solo developer feel like they have a disciplined growth analyst reviewing their app every day.

## 2. Problem Statement

Android developers often launch an app and then struggle to answer basic growth questions:

- Are people finding the store listing?
- Are visitors converting into installs?
- Are installs coming from the right countries?
- Are users retaining after installation?
- Are crashes or ANRs hurting user trust?
- Are reviews exposing repeated product problems?
- Are ads bringing quality users or wasting money?
- Is the Play Store listing honest, clear, and convincing?
- Which change should be tested next?
- Did the last manual change help or harm growth?

Most developers have fragmented data across Play Console, Firebase/GA4, Android vitals, Google Ads, notes, screenshots, and reviews. They need diagnosis and prioritization more than automation.

## 3. Target Users

### Primary Users

- Indie Android developers
- Solo game developers
- Small studios
- Early-stage app founders
- Developers launching their first Google Play app

### Initial Internal User

The first internal app is an offline-first mini arcade game containing:

1. Pulse Orbit
2. Lane Drift
3. Stack Drop

The game should be positioned honestly as lightweight, offline-first, quick-session, low-end Android friendly, and non-aggressively monetized.

## 4. Product Principles

### The System Must Be

- Evidence-driven
- Human-controlled
- Recommendation-first
- Simple enough for a solo developer
- Honest about confidence and limitations
- Conservative with store and ads advice
- Focused on quality growth, not vanity numbers
- Useful before API integrations exist

### The System Must Avoid

- Fake reviews
- Fake installs
- Keyword stuffing
- Misleading claims
- Competitor keyword abuse
- Aggressive monetization pressure
- Daily chaotic listing changes
- Unjustified ad spending
- Automated production changes

## 5. MVP-0 Goal

Build a working local/manual-data growth copilot that can:

1. Store app profile and positioning.
2. Accept manual daily metrics and CSV imports.
3. Store Play review excerpts and ratings.
4. Store crash/vitals summaries.
5. Store ads summary metrics.
6. Show a dashboard of growth signals.
7. Generate rule-based bottleneck diagnosis.
8. Generate AI-assisted daily/weekly reports.
9. Create recommendation cards with evidence and next steps.
10. Suggest Play Store listing improvements.
11. Analyze reviews into themes.
12. Build structured experiment plans.
13. Log what the developer manually changed.
14. Track before/after outcomes.
15. Maintain an audit trail of AI outputs and user decisions.

## 6. MVP-0 Scope

### Included

- Single-user or simple admin login
- App profile management
- Manual data entry forms
- CSV import templates
- Dashboard
- Recommendation queue
- Review analyzer
- Listing advisor
- Experiment planner
- Manual action log
- Outcome tracker
- Audit log
- Demo seed data for the arcade game
- AI provider abstraction with a mock provider fallback

### Not Included

- Google Play Console write integration
- Google Ads write integration
- Automatic review replies
- Automatic screenshot generation/upload
- Automatic title/description edits
- Automatic publishing
- Multi-tenant SaaS billing
- Public onboarding
- Autonomous growth execution

## 7. Recommendation Philosophy

A recommendation must answer:

- What is the problem?
- What evidence supports it?
- What exact human action should be taken?
- What should not be done yet?
- How risky is it?
- How much effort is required?
- What metric should be watched afterward?
- When should the decision be reviewed?

## 8. Success Criteria

MVP-0 is successful when it can:

- Import or manually enter 7–30 days of app data.
- Identify the most likely bottleneck.
- Generate a clear growth report.
- Suggest safe listing improvements.
- Extract review themes.
- Create at least three experiment ideas.
- Let the developer mark recommendations as accepted, rejected, implemented, or monitoring.
- Track manual actions against later outcomes.
- Run locally through Docker Compose.

## 9. First Internal Success Target

For the arcade game, the product should help answer:

- Is the Play Store listing converting?
- Are screenshots clearly explaining Pulse Orbit, Lane Drift, and Stack Drop?
- Is offline-first positioning visible enough?
- Is the app lightweight positioning believable?
- Are users complaining about controls, crashes, difficulty, boredom, or confusion?
- Should the next action be listing improvement, product fix, review response, or ad testing?
