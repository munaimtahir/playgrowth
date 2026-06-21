from django.contrib import admin
from .models import (
    AdCampaignMetric,
    AndroidVitalsMetric,
    AppProfile,
    AuditLog,
    CountryMetric,
    DailyMetric,
    DataImportBatch,
    Experiment,
    GrowthReport,
    ManualActionLog,
    Recommendation,
    ReviewItem,
    ReviewTheme,
    StoreListingSnapshot,
)

for model in [
    AppProfile,
    DataImportBatch,
    DailyMetric,
    CountryMetric,
    StoreListingSnapshot,
    ReviewItem,
    ReviewTheme,
    AndroidVitalsMetric,
    AdCampaignMetric,
    GrowthReport,
    Recommendation,
    Experiment,
    ManualActionLog,
    AuditLog,
]:
    admin.site.register(model)
