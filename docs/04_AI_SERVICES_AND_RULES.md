# AI Services and Decision Rules — PlayGrowth Copilot v2

## 1. AI Role

AI is used for interpretation, drafting, summarization, and structured recommendations.

AI does not execute production changes.

## 2. AI Service Layer

The backend should expose clean service classes:

### GrowthAnalysisService

Purpose:

- Analyze metrics
- Identify likely bottleneck
- Generate daily/weekly report
- Recommend next human actions

Inputs:

- AppProfile
- DailyMetric
- CountryMetric
- AndroidVitalsMetric
- AdCampaignMetric
- ReviewTheme
- StoreListingSnapshot
- ManualActionLog

Outputs:

- GrowthReport
- Recommendation cards

### ReviewAnalysisService

Purpose:

- Classify reviews
- Detect repeated complaints
- Extract praise
- Draft optional manual reply text
- Identify product fixes before marketing pushes

Categories:

- bug/crash
- performance
- controls
- difficulty
- confusion
- ads/monetization
- offline issue
- praise
- feature request
- pricing
- other

### ListingAdvisorService

Purpose:

- Suggest clearer Play Store text
- Draft honest short descriptions
- Draft full description sections
- Suggest screenshot captions
- Suggest feature graphic concepts
- Identify keyword stuffing risk

### ExperimentPlannerService

Purpose:

- Convert a recommendation into a testable manual experiment.

### AdsAdvisorService

Purpose:

- Analyze imported ads metrics
- Warn against spending when conversion/retention/quality is weak
- Suggest manual campaign cleanup or observation plans

### PolicySafetyService

Purpose:

- Reject or flag unsafe suggestions.

## 3. Policy Safety Rules

Block or warn against:

- Fake installs
- Fake reviews
- Incentivized reviews
- Keyword stuffing
- Competitor trademark misuse
- “Best”, “#1”, “top rated” without evidence
- “No ads” if ads exist
- “Fully offline” if meaningful features require internet
- Misleading screenshots
- Exaggerated performance claims
- Aggressive spending when retention is weak
- Daily random listing changes without experiment tracking

## 4. Bottleneck Diagnosis Rules

| Signal | Likely Diagnosis | Recommended Human Action |
|---|---|---|
| Low impressions and low visitors | Discovery problem | Improve ASO structure and metadata clarity |
| Visitors adequate but install conversion low | Store conversion problem | Improve screenshots, short description, value proposition |
| Installs adequate but D1 retention low | Product/onboarding problem | Improve first-run experience and core loop clarity |
| Reviews mention controls repeatedly | UX/control clarity problem | Fix controls before scaling ads |
| Crash/ANR rate high | Quality problem | Fix stability before listing/ads push |
| Ads CPI high and conversion low | Ads/listing mismatch | Pause scale; refine store listing and targeting manually |
| Good retention but low visitors | Visibility problem | Improve organic discovery and consider small manual ad tests |
| High uninstalls | Expectation mismatch or quality issue | Compare listing promise with actual experience |

## 5. Recommendation Format

Every recommendation must include:

```json
{
  "category": "store_listing | product_quality | retention | reviews | ads | experiment",
  "title": "Clear short title",
  "diagnosis": "What seems wrong",
  "evidence": ["Metric or review signal"],
  "suggested_human_action": "Exact action the developer should perform manually",
  "copyable_text": "Optional draft text/caption/reply",
  "do_not_do_yet": "Unsafe or premature action to avoid",
  "expected_impact": "What may improve",
  "watch_metric": "Metric to monitor",
  "risk_level": "low | medium | high",
  "effort_level": "low | medium | high",
  "confidence_score": 0.0
}
```

## 6. Prompting Principles

AI prompts should:

- Include app positioning.
- Include only relevant metric windows.
- Ask for conservative recommendations.
- Require evidence for each claim.
- Require exact next action.
- Require “do not do yet” guidance.
- Reject fake or manipulative growth tactics.
- Prefer fewer prioritized actions over long generic lists.

## 7. Example Recommendation

### Signal

Visitors are present, but conversion rate is weak. Reviews are not yet enough to identify product themes.

### Diagnosis

Store listing value proposition may not be clear enough.

### Human Action

Manually update the first screenshot caption to explain the core value faster:

> “3 quick arcade games. Works offline. Play in short breaks.”

### Do Not Do Yet

Do not increase ad budget until listing conversion improves.

### Watch Metric

Store listing conversion rate over the next 7–14 days.
