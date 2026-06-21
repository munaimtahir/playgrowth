# Executive Summary — PlayGrowth Copilot v2

## What We Are Building

PlayGrowth Copilot is a private growth command center for Android app developers. It brings app growth data, reviews, store listing notes, crash/vitals summaries, ads summaries, and experiment history into one dashboard, then uses AI and rules to explain what is happening and what the developer should do next.

## What Changed from the Earlier Concept

The product is no longer framed as an automation system that prepares or performs external changes. The new concept is a **controlled recommendation and tracking system**.

### Old Direction

- AI prepares changes.
- Approval workflow is central.
- Future integrations may write to Play Console or Ads.
- The product could become semi-autonomous.

### New Direction

- AI analyzes, diagnoses, and suggests.
- The developer manually implements changes outside the system.
- The system records what was suggested, what the developer did, and whether metrics improved.
- No Play Console writes, screenshot uploads, ad budget changes, campaign launches, or production publishing from the MVP.

## Product Role

The product is best understood as an:

- ASO analyst
- growth analyst
- product-quality analyst
- review analyst
- ads advisor
- experiment planner
- decision log

It is not an autonomous marketing bot.

## MVP Definition

MVP-0 should work without external Google API integrations. It should support manual data input and CSV imports so the product logic can be validated before adding integrations.

## Primary Jobs-to-be-Done

1. Tell me whether my app has a visibility, conversion, retention, quality, or ads problem.
2. Tell me what exact change I should make next.
3. Help me improve my Play Store listing without misleading users.
4. Extract useful themes from Play reviews.
5. Help me plan experiments I can manually run.
6. Track whether my manual changes improved outcomes.

## Non-negotiable Constraints

- No fake installs.
- No fake reviews.
- No keyword stuffing.
- No competitor-name misuse.
- No exaggerated claims.
- No auto-publishing.
- No automatic ad-budget increase.
- No direct production writes in MVP.
- Every recommendation must include evidence, confidence, effort, risk, and a suggested next action.
