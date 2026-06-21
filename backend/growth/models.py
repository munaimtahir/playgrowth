from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AppProfile(TimeStampedModel):
    name = models.CharField(max_length=200)
    package_name = models.CharField(max_length=255, unique=True)
    play_store_url = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    app_type = models.CharField(max_length=100, blank=True)
    primary_positioning = models.TextField(blank=True)
    target_countries = models.TextField(blank=True)
    monetization_model = models.CharField(max_length=200, blank=True)
    current_version = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DataImportBatch(TimeStampedModel):
    IMPORT_TYPES = [
        ('daily_metrics', 'Daily metrics'),
        ('country_metrics', 'Country metrics'),
        ('reviews', 'Reviews'),
        ('android_vitals', 'Android vitals'),
        ('ads', 'Ads'),
        ('listing_snapshot', 'Listing snapshot'),
    ]
    STATUSES = [('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')]

    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='import_batches')
    import_type = models.CharField(max_length=50, choices=IMPORT_TYPES)
    source_filename = models.CharField(max_length=255, blank=True)
    source_label = models.CharField(max_length=255, blank=True)
    row_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    error_summary = models.TextField(blank=True)

    def __str__(self):
        return f'{self.app} - {self.import_type} - {self.created_at:%Y-%m-%d}'


class DailyMetric(TimeStampedModel):
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='daily_metrics')
    date = models.DateField()
    installs = models.IntegerField(default=0)
    uninstalls = models.IntegerField(default=0)
    store_visitors = models.IntegerField(default=0)
    listing_conversion_rate = models.FloatField(null=True, blank=True)
    active_users = models.IntegerField(default=0)
    day_1_retention = models.FloatField(null=True, blank=True)
    day_7_retention = models.FloatField(null=True, blank=True)
    average_session_length = models.FloatField(null=True, blank=True)
    game_starts = models.IntegerField(default=0)
    retry_count = models.IntegerField(default=0)
    daily_challenge_opens = models.IntegerField(default=0)
    daily_challenge_completions = models.IntegerField(default=0)
    premium_clicks = models.IntegerField(default=0)
    premium_purchases = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    import_batch = models.ForeignKey(DataImportBatch, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('app', 'date')
        ordering = ['-date']


class CountryMetric(TimeStampedModel):
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='country_metrics')
    date = models.DateField()
    country_code = models.CharField(max_length=8)
    installs = models.IntegerField(default=0)
    visitors = models.IntegerField(default=0)
    conversion_rate = models.FloatField(null=True, blank=True)
    retention_d1 = models.FloatField(null=True, blank=True)
    retention_d7 = models.FloatField(null=True, blank=True)
    ad_spend = models.FloatField(default=0)
    cpi = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    import_batch = models.ForeignKey(DataImportBatch, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('app', 'date', 'country_code')


class StoreListingSnapshot(TimeStampedModel):
    STATUSES = [('current', 'Current'), ('draft', 'Draft'), ('historical', 'Historical'), ('proposed', 'Proposed')]
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='listing_snapshots')
    snapshot_date = models.DateField()
    app_title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True)
    full_description = models.TextField(blank=True)
    screenshot_notes = models.TextField(blank=True)
    feature_graphic_notes = models.TextField(blank=True)
    video_notes = models.TextField(blank=True)
    language = models.CharField(max_length=20, default='en')
    status = models.CharField(max_length=20, choices=STATUSES, default='current')
    notes = models.TextField(blank=True)


class ReviewItem(TimeStampedModel):
    STATUSES = [
        ('new', 'New'),
        ('analyzed', 'Analyzed'),
        ('needs_product_fix', 'Needs product fix'),
        ('reply_drafted', 'Reply drafted'),
        ('manually_replied', 'Manually replied'),
        ('ignored', 'Ignored'),
    ]
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='reviews')
    review_external_id = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    rating = models.PositiveSmallIntegerField(default=0)
    reviewer_name = models.CharField(max_length=255, blank=True)
    review_text = models.TextField()
    device = models.CharField(max_length=255, blank=True)
    app_version = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=20, default='en')
    sentiment = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=100, blank=True)
    ai_summary = models.TextField(blank=True)
    suggested_reply = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUSES, default='new')
    import_batch = models.ForeignKey(DataImportBatch, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date']


class ReviewTheme(TimeStampedModel):
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='review_themes')
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    category = models.CharField(max_length=100)
    theme = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)
    severity = models.CharField(max_length=50, default='medium')
    examples_json = models.JSONField(default=list, blank=True)
    recommendation = models.TextField(blank=True)


class AndroidVitalsMetric(TimeStampedModel):
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='vitals')
    date = models.DateField()
    crash_rate = models.FloatField(null=True, blank=True)
    anr_rate = models.FloatField(null=True, blank=True)
    slow_rendering_rate = models.FloatField(null=True, blank=True)
    excessive_wakeups = models.FloatField(null=True, blank=True)
    affected_devices_json = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    import_batch = models.ForeignKey(DataImportBatch, on_delete=models.SET_NULL, null=True, blank=True)


class AdCampaignMetric(TimeStampedModel):
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='ads')
    date = models.DateField()
    campaign_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=8, blank=True)
    spend = models.FloatField(default=0)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    installs = models.IntegerField(default=0)
    cpi = models.FloatField(null=True, blank=True)
    conversions = models.IntegerField(default=0)
    retention_d1 = models.FloatField(null=True, blank=True)
    retention_d7 = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    import_batch = models.ForeignKey(DataImportBatch, on_delete=models.SET_NULL, null=True, blank=True)


class GrowthReport(TimeStampedModel):
    REPORT_TYPES = [('daily', 'Daily'), ('weekly', 'Weekly'), ('custom', 'Custom')]
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='growth_reports')
    report_date = models.DateField(auto_now_add=True)
    period_start = models.DateField()
    period_end = models.DateField()
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='weekly')
    summary = models.TextField()
    bottleneck = models.CharField(max_length=255, blank=True)
    evidence_json = models.JSONField(default=list, blank=True)
    next_actions_json = models.JSONField(default=list, blank=True)
    confidence_score = models.FloatField(default=0)
    ai_provider = models.CharField(max_length=100, default='mock')


class Recommendation(TimeStampedModel):
    STATUSES = [
        ('suggested', 'Suggested'),
        ('accepted_to_try', 'Accepted to try'),
        ('rejected', 'Rejected'),
        ('manually_implemented', 'Manually implemented'),
        ('monitoring', 'Monitoring'),
        ('successful', 'Successful'),
        ('unsuccessful', 'Unsuccessful'),
        ('closed', 'Closed'),
    ]
    RISK_LEVELS = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    EFFORT_LEVELS = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='recommendations')
    source_report = models.ForeignKey(GrowthReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='recommendations')
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    diagnosis = models.TextField(blank=True)
    evidence_json = models.JSONField(default=list, blank=True)
    suggested_human_action = models.TextField()
    copyable_text = models.TextField(blank=True)
    do_not_do_yet = models.TextField(blank=True)
    expected_impact = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='low')
    effort_level = models.CharField(max_length=20, choices=EFFORT_LEVELS, default='low')
    confidence_score = models.FloatField(default=0)
    status = models.CharField(max_length=30, choices=STATUSES, default='suggested')
    watch_metric = models.CharField(max_length=255, blank=True)
    review_after_days = models.PositiveIntegerField(default=7)
    accepted_at = models.DateTimeField(null=True, blank=True)
    implemented_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    result_summary = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']


class Experiment(TimeStampedModel):
    STATUSES = [('idea', 'Idea'), ('planned', 'Planned'), ('running_manually', 'Running manually'), ('completed', 'Completed'), ('stopped', 'Stopped'), ('archived', 'Archived')]
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='experiments')
    name = models.CharField(max_length=255)
    hypothesis = models.TextField()
    area = models.CharField(max_length=100, blank=True)
    variant_a = models.TextField(blank=True)
    variant_b = models.TextField(blank=True)
    primary_metric = models.CharField(max_length=255)
    secondary_metric = models.CharField(max_length=255, blank=True)
    minimum_duration_days = models.PositiveIntegerField(default=7)
    minimum_sample_size = models.PositiveIntegerField(default=100)
    success_rule = models.TextField(blank=True)
    failure_rule = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUSES, default='idea')
    result = models.TextField(blank=True)
    decision = models.TextField(blank=True)


class ManualActionLog(TimeStampedModel):
    ACTION_TYPES = [
        ('listing_text_change', 'Listing text change'),
        ('screenshot_change', 'Screenshot change'),
        ('feature_graphic_change', 'Feature graphic change'),
        ('app_update', 'App update'),
        ('bug_fix', 'Bug fix'),
        ('control_improvement', 'Control improvement'),
        ('ads_change', 'Ads change'),
        ('review_response', 'Review response'),
        ('experiment_started', 'Experiment started'),
        ('experiment_ended', 'Experiment ended'),
        ('other', 'Other'),
    ]
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, related_name='manual_actions')
    recommendation = models.ForeignKey(Recommendation, on_delete=models.SET_NULL, null=True, blank=True, related_name='manual_actions')
    action_date = models.DateField()
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    changed_location = models.CharField(max_length=255, blank=True)
    before_text = models.TextField(blank=True)
    after_text = models.TextField(blank=True)
    expected_metric = models.CharField(max_length=255, blank=True)
    followup_date = models.DateField(null=True, blank=True)
    outcome_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-action_date']


class AuditLog(models.Model):
    app = models.ForeignKey(AppProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='audit_logs')
    actor = models.CharField(max_length=255, default='system')
    event_type = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    summary = models.TextField()
    metadata_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
