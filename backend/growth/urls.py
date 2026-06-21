from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    AdCampaignMetricViewSet,
    AndroidVitalsMetricViewSet,
    AppProfileViewSet,
    AuditLogViewSet,
    CountryMetricViewSet,
    DailyMetricViewSet,
    DataImportBatchViewSet,
    ExperimentViewSet,
    GrowthReportViewSet,
    ManualActionLogViewSet,
    RecommendationViewSet,
    ReviewItemViewSet,
    ReviewThemeViewSet,
    StoreListingSnapshotViewSet,
    analyze_reviews_view,
    api_root,
    dashboard_summary,
    listing_advisor_generate,
    import_daily_metrics_view,
    import_reviews_view,
)

router = DefaultRouter()
router.register('apps', AppProfileViewSet)
router.register('import-batches', DataImportBatchViewSet)
router.register('daily-metrics', DailyMetricViewSet)
router.register('country-metrics', CountryMetricViewSet)
router.register('listing-snapshots', StoreListingSnapshotViewSet)
router.register('reviews', ReviewItemViewSet)
router.register('review-themes', ReviewThemeViewSet)
router.register('android-vitals', AndroidVitalsMetricViewSet)
router.register('ads', AdCampaignMetricViewSet)
router.register('growth-reports', GrowthReportViewSet)
router.register('recommendations', RecommendationViewSet)
router.register('experiments', ExperimentViewSet)
router.register('manual-actions', ManualActionLogViewSet)
router.register('audit-logs', AuditLogViewSet)

urlpatterns = [
    path('', api_root),
    path('dashboard/summary/', dashboard_summary),
    path('imports/daily-metrics/', import_daily_metrics_view),
    path('imports/reviews/', import_reviews_view),
    path('listing-advisor/generate/', listing_advisor_generate),
    path('reviews/analyze/', analyze_reviews_view),
] + router.urls
