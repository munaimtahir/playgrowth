# Data Model — PlayGrowth Copilot v2

## 1. Core Concepts

The data model is designed around five loops:

1. App identity
2. Growth signal tracking
3. Diagnosis and recommendations
4. Manual implementation logging
5. Outcome review

## 2. Models

### AppProfile

Stores the app being tracked.

Fields:

- id
- name
- package_name
- play_store_url
- category
- app_type
- primary_positioning
- target_countries
- monetization_model
- current_version
- notes
- created_at
- updated_at

### DataImportBatch

Tracks manual imports.

Fields:

- id
- app
- import_type
- source_filename
- source_label
- row_count
- status
- error_summary
- created_at

Import types:

- daily_metrics
- country_metrics
- reviews
- android_vitals
- ads
- listing_snapshot

### DailyMetric

One row per app per date.

Fields:

- id
- app
- date
- installs
- uninstalls
- store_visitors
- listing_conversion_rate
- active_users
- day_1_retention
- day_7_retention
- average_session_length
- game_starts
- retry_count
- daily_challenge_opens
- daily_challenge_completions
- premium_clicks
- premium_purchases
- notes
- import_batch
- created_at

### CountryMetric

Fields:

- id
- app
- date
- country_code
- installs
- visitors
- conversion_rate
- retention_d1
- retention_d7
- ad_spend
- cpi
- notes
- import_batch

### StoreListingSnapshot

Stores the listing at a point in time.

Fields:

- id
- app
- snapshot_date
- app_title
- short_description
- full_description
- screenshot_notes
- feature_graphic_notes
- video_notes
- language
- status
- notes
- created_at

Statuses:

- current
- draft
- historical
- proposed

### ReviewItem

Fields:

- id
- app
- review_external_id
- date
- rating
- reviewer_name
- review_text
- device
- app_version
- language
- sentiment
- category
- ai_summary
- suggested_reply
- status
- import_batch
- created_at

Review statuses:

- new
- analyzed
- needs_product_fix
- reply_drafted
- manually_replied
- ignored

### ReviewTheme

Aggregated issue or praise cluster.

Fields:

- id
- app
- date_range_start
- date_range_end
- category
- theme
- count
- severity
- examples_json
- recommendation
- created_at

### AndroidVitalsMetric

Fields:

- id
- app
- date
- crash_rate
- anr_rate
- slow_rendering_rate
- excessive_wakeups
- affected_devices_json
- notes
- import_batch

### AdCampaignMetric

Fields:

- id
- app
- date
- campaign_name
- country_code
- spend
- impressions
- clicks
- installs
- cpi
- conversions
- retention_d1
- retention_d7
- notes
- import_batch

### GrowthReport

AI/rule-generated report.

Fields:

- id
- app
- report_date
- period_start
- period_end
- report_type
- summary
- bottleneck
- evidence_json
- next_actions_json
- confidence_score
- ai_provider
- created_at

Report types:

- daily
- weekly
- custom

### Recommendation

A human action suggestion.

Fields:

- id
- app
- source_report
- date
- category
- title
- diagnosis
- evidence_json
- suggested_human_action
- copyable_text
- do_not_do_yet
- expected_impact
- risk_level
- effort_level
- confidence_score
- status
- watch_metric
- review_after_days
- created_at
- accepted_at
- implemented_at
- closed_at
- result_summary

Statuses:

- suggested
- accepted_to_try
- rejected
- manually_implemented
- monitoring
- successful
- unsuccessful
- closed

Important: these statuses do not trigger external API writes.

### Experiment

Fields:

- id
- app
- name
- hypothesis
- area
- variant_a
- variant_b
- primary_metric
- secondary_metric
- minimum_duration_days
- minimum_sample_size
- success_rule
- failure_rule
- start_date
- end_date
- status
- result
- decision
- created_at

Statuses:

- idea
- planned
- running_manually
- completed
- stopped
- archived

### ManualActionLog

Records what the developer manually changed.

Fields:

- id
- app
- recommendation
- action_date
- action_type
- title
- description
- changed_location
- before_text
- after_text
- expected_metric
- followup_date
- outcome_notes
- created_at

Action types:

- listing_text_change
- screenshot_change
- feature_graphic_change
- app_update
- bug_fix
- control_improvement
- ads_change
- review_response
- experiment_started
- experiment_ended
- other

### AuditLog

Fields:

- id
- app
- actor
- event_type
- object_type
- object_id
- summary
- metadata_json
- created_at

## 3. MVP Relationships

- AppProfile has many DailyMetric rows.
- AppProfile has many ReviewItem rows.
- AppProfile has many Recommendation rows.
- GrowthReport can create many Recommendations.
- Recommendation can have zero or more ManualActionLog rows.
- Experiment can be linked to recommendations later.

## 4. Seed Data for Internal App

Create one AppProfile:

- name: Offline Mini Arcade
- app_type: Game
- category: Arcade
- package_name: placeholder until final package is added
- primary_positioning: Lightweight offline-first mini arcade with Pulse Orbit, Lane Drift, and Stack Drop.
- target_countries: Pakistan, India, Philippines, Indonesia, United States, United Kingdom
- monetization_model: Free / non-aggressive monetization
