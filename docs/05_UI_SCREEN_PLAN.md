# UI Screen Plan — PlayGrowth Copilot v2

## 1. Navigation

Primary sidebar:

1. Dashboard
2. App Profile
3. Data Import
4. Growth Reports
5. Recommendations
6. Reviews
7. Listing Advisor
8. Experiments
9. Action Log
10. Settings

## 2. Dashboard

Purpose:
Show the current growth state at a glance.

Sections:

- Selected app
- Date range selector
- KPI cards
  - installs
  - visitors
  - conversion rate
  - D1 retention
  - D7 retention
  - average rating
  - crash rate
  - ad spend
  - CPI
- Growth trend chart
- Bottleneck card
- Top recommendations
- Recent manual actions
- Data freshness warnings

## 3. App Profile

Purpose:
Store the app identity and positioning used by the AI.

Fields:

- App name
- Package name
- Play Store URL
- Category
- App type
- Target countries
- Monetization model
- Positioning statement
- Notes

For the initial app, include structured positioning chips:

- Offline-first
- Lightweight
- Quick sessions
- Low-end Android friendly
- 3 mini games
- No aggressive monetization

## 4. Data Import

Purpose:
Support manual-first MVP.

Sections:

- Add daily metric manually
- Upload daily metrics CSV
- Upload reviews CSV
- Upload Android vitals CSV
- Upload ads summary CSV
- Import history
- Download CSV templates

## 5. Growth Reports

Purpose:
Show AI/rule-generated reports.

Report card sections:

- Summary
- Main bottleneck
- Evidence
- What changed since previous period
- What to do next
- What not to do yet
- Confidence

Actions:

- Generate report
- Create recommendations from report
- Export as markdown

## 6. Recommendations

Purpose:
A prioritized work queue for the developer.

Columns or filters:

- Suggested
- Accepted to try
- Manually implemented
- Monitoring
- Successful/Unsuccessful
- Rejected/Closed

Recommendation card:

- Title
- Category
- Evidence
- Suggested human action
- Copyable text
- Do not do yet
- Expected impact
- Watch metric
- Risk
- Effort
- Confidence
- Status buttons
- Create manual action log

## 7. Reviews

Purpose:
Turn reviews into product/growth intelligence.

Sections:

- Rating distribution
- Review list
- AI themes
- Repeated complaints
- Praise themes
- Reply drafts for manual use
- Product fix suggestions

## 8. Listing Advisor

Purpose:
Generate safe, honest listing improvements.

Sections:

- Current listing snapshot
- Short description drafts
- Full description structure
- Screenshot caption ideas
- Feature graphic ideas
- ASO clarity checklist
- Policy safety warnings

Important:
The user copies suggestions manually into Play Console. There is no publish button.

## 9. Experiments

Purpose:
Plan manual experiments.

Experiment fields:

- Hypothesis
- Area
- Variant A
- Variant B
- Primary metric
- Secondary metric
- Minimum duration
- Success rule
- Failure rule
- Status
- Decision

## 10. Action Log

Purpose:
Record what the developer actually changed outside the system.

Examples:

- Changed short description
- Uploaded new screenshot set
- Updated app controls
- Fixed crash
- Paused ad campaign manually
- Started Play Console store listing experiment manually

## 11. Settings

Purpose:
Configure the local product.

Sections:

- AI provider setting
- API base URL
- Data retention preferences
- Safety mode
- Export/backup
