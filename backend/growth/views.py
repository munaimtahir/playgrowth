from __future__ import annotations

from datetime import date, timedelta

from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .importers import import_daily_metrics, import_reviews
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
from .serializers import (
    AdCampaignMetricSerializer,
    AndroidVitalsMetricSerializer,
    AppProfileSerializer,
    AuditLogSerializer,
    CountryMetricSerializer,
    DailyMetricSerializer,
    DataImportBatchSerializer,
    ExperimentSerializer,
    GrowthReportSerializer,
    ManualActionLogSerializer,
    RecommendationSerializer,
    ReviewItemSerializer,
    ReviewThemeSerializer,
    StoreListingSnapshotSerializer,
)
from .services.ai import get_ai_provider
from .services.diagnosis import BottleneckDiagnosisService
from .services.reports import GrowthReportService
from .services.reviews import ReviewAnalysisService


def _selected_app(request):
    app_id = request.query_params.get('app')
    if not app_id and hasattr(request, 'data'):
        app_id = request.data.get('app')
    if app_id:
        return get_object_or_404(AppProfile, pk=app_id)
    return AppProfile.objects.order_by('name', 'id').first()


def _recent_window(app, days=7):
    latest_date = app.daily_metrics.order_by('-date').values_list('date', flat=True).first() or date.today()
    return latest_date - timedelta(days=days - 1), latest_date


def _recommendation_queryset(app):
    priority_rank = {'high': 0, 'medium': 1, 'low': 2}
    return sorted(
        app.recommendations.all(),
        key=lambda rec: (
            priority_rank.get(rec.priority, 1),
            -float(rec.confidence_score or 0),
            -(rec.created_at.timestamp() if rec.created_at else 0),
        ),
    )


class AppProfileViewSet(viewsets.ModelViewSet):
    queryset = AppProfile.objects.all().order_by('name')
    serializer_class = AppProfileSerializer
    filterset_fields = ['package_name', 'category', 'app_type']


class DataImportBatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataImportBatch.objects.select_related('app').all()
    serializer_class = DataImportBatchSerializer
    filterset_fields = ['app', 'import_type', 'status']


class DailyMetricViewSet(viewsets.ModelViewSet):
    queryset = DailyMetric.objects.select_related('app').all()
    serializer_class = DailyMetricSerializer
    filterset_fields = ['app', 'date']


class CountryMetricViewSet(viewsets.ModelViewSet):
    queryset = CountryMetric.objects.select_related('app').all()
    serializer_class = CountryMetricSerializer
    filterset_fields = ['app', 'date', 'country_code']


class StoreListingSnapshotViewSet(viewsets.ModelViewSet):
    queryset = StoreListingSnapshot.objects.select_related('app').all()
    serializer_class = StoreListingSnapshotSerializer
    filterset_fields = ['app', 'status', 'language']


class ReviewItemViewSet(viewsets.ModelViewSet):
    queryset = ReviewItem.objects.select_related('app').all()
    serializer_class = ReviewItemSerializer
    filterset_fields = ['app', 'rating', 'category', 'status']


class ReviewThemeViewSet(viewsets.ModelViewSet):
    queryset = ReviewTheme.objects.select_related('app').all()
    serializer_class = ReviewThemeSerializer
    filterset_fields = ['app', 'category', 'severity']


class AndroidVitalsMetricViewSet(viewsets.ModelViewSet):
    queryset = AndroidVitalsMetric.objects.select_related('app').all()
    serializer_class = AndroidVitalsMetricSerializer
    filterset_fields = ['app', 'date']


class AdCampaignMetricViewSet(viewsets.ModelViewSet):
    queryset = AdCampaignMetric.objects.select_related('app').all()
    serializer_class = AdCampaignMetricSerializer
    filterset_fields = ['app', 'date', 'country_code', 'campaign_name']


class GrowthReportViewSet(viewsets.ModelViewSet):
    queryset = GrowthReport.objects.select_related('app').all()
    serializer_class = GrowthReportSerializer
    filterset_fields = ['app', 'report_type', 'bottleneck']

    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        app = get_object_or_404(AppProfile, pk=request.data['app'])
        period_end = date.fromisoformat(request.data.get('period_end')) if request.data.get('period_end') else date.today()
        period_start = date.fromisoformat(request.data.get('period_start')) if request.data.get('period_start') else period_end - timedelta(days=7)
        report_type = request.data.get('report_type', 'weekly')
        report = GrowthReportService().generate(app, period_start, period_end, report_type=report_type)
        AuditLog.objects.create(
            app=app,
            actor='user',
            event_type='growth_report_generated',
            object_type='GrowthReport',
            object_id=str(report.id),
            summary=f'Generated {report_type} report for {app.name}',
        )
        return Response(GrowthReportSerializer(report).data, status=status.HTTP_201_CREATED)


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.select_related('app', 'source_report').all()
    serializer_class = RecommendationSerializer
    filterset_fields = ['app', 'status', 'category', 'risk_level', 'effort_level']

    def _set_status(self, next_status, timestamp_field=None):
        rec = self.get_object()
        rec.status = next_status
        if timestamp_field:
            setattr(rec, timestamp_field, timezone.now())
        rec.save()
        AuditLog.objects.create(
            app=rec.app,
            actor='user',
            event_type=f'recommendation_{next_status}',
            object_type='Recommendation',
            object_id=str(rec.id),
            summary=rec.title,
        )
        return Response(self.get_serializer(rec).data)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        return self._set_status('accepted', 'accepted_at')

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        return self._set_status('rejected')

    @action(detail=True, methods=['post'])
    def done(self, request, pk=None):
        return self._set_status('done', 'implemented_at')

    @action(detail=True, methods=['post'])
    def monitoring(self, request, pk=None):
        return self._set_status('monitoring')


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.select_related('app').all()
    serializer_class = ExperimentSerializer
    filterset_fields = ['app', 'status', 'area']


class ManualActionLogViewSet(viewsets.ModelViewSet):
    queryset = ManualActionLog.objects.select_related('app', 'recommendation').all()
    serializer_class = ManualActionLogSerializer
    filterset_fields = ['app', 'action_type', 'recommendation']


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('app').all()
    serializer_class = AuditLogSerializer
    filterset_fields = ['app', 'event_type', 'object_type']


@api_view(['GET'])
def api_root(request):
    return Response(
        {
            'name': 'PlayGrowth Copilot API',
            'status': 'ok',
            'version': 'v1',
            'endpoints': {
                'health': '/api/health/',
                'dashboard_summary': '/api/v1/dashboard/summary/',
                'apps': '/api/v1/apps/',
                'reports': '/api/v1/growth-reports/',
                'recommendations': '/api/v1/recommendations/',
                'listing_advisor': '/api/v1/listing-advisor/generate/',
                'review_analysis': '/api/v1/reviews/analyze/',
            },
        }
    )


@api_view(['GET'])
def dashboard_summary(request):
    app = _selected_app(request)
    if not app:
        return Response({'detail': 'Create an app profile first.'}, status=status.HTTP_404_NOT_FOUND)

    window_start, window_end = _recent_window(app, days=7)
    metrics = app.daily_metrics.filter(date__gte=window_start, date__lte=window_end).order_by('date')
    vitals = app.vitals.filter(date__gte=window_start, date__lte=window_end)
    ads = app.ads.filter(date__gte=window_start, date__lte=window_end)
    reviews = app.reviews.filter(date__gte=window_start, date__lte=window_end)

    aggregate = metrics.aggregate(
        installs=Sum('installs'),
        visitors=Sum('store_visitors'),
        conversion=Avg('listing_conversion_rate'),
        d1=Avg('day_1_retention'),
        d7=Avg('day_7_retention'),
        avg_active_users=Avg('active_users'),
        avg_session=Avg('average_session_length'),
    )
    review_aggregate = reviews.aggregate(
        count=Count('id'),
        avg_rating=Avg('rating'),
    )
    ad_aggregate = ads.aggregate(
        spend=Sum('spend'),
        installs=Sum('installs'),
        clicks=Sum('clicks'),
    )
    vitals_aggregate = vitals.aggregate(
        crash_rate=Avg('crash_rate'),
        anr_rate=Avg('anr_rate'),
    )

    diagnosis = BottleneckDiagnosisService().diagnose(metrics, vitals=vitals, ads=ads, reviews=reviews)
    latest_report = app.growth_reports.order_by('-created_at').first()
    recommendations = list(_recommendation_queryset(app))
    next_recommendation = recommendations[0] if recommendations else None
    recent_actions = app.manual_actions.all()[:5]
    review_themes = app.review_themes.all()[:5]

    return Response(
        {
            'app': AppProfileSerializer(app).data,
            'window': {'start': window_start, 'end': window_end},
            'kpis': {
                'installs': aggregate['installs'] or 0,
                'store_visitors': aggregate['visitors'] or 0,
                'conversion_rate': round(aggregate['conversion'] or 0, 2),
                'day_1_retention': round(aggregate['d1'] or 0, 2),
                'day_7_retention': round(aggregate['d7'] or 0, 2),
                'reviews': review_aggregate['count'] or 0,
                'rating': round(review_aggregate['avg_rating'] or 0, 2),
                'crashes': round(vitals_aggregate['crash_rate'] or 0, 2),
                'anrs': round(vitals_aggregate['anr_rate'] or 0, 2),
                'ads_spend': round(ad_aggregate['spend'] or 0, 2),
                'cpi': round((ad_aggregate['spend'] / ad_aggregate['installs']) if ad_aggregate['spend'] and ad_aggregate['installs'] else 0, 2),
                'active_users': round(aggregate['avg_active_users'] or 0, 2),
                'average_session_length': round(aggregate['avg_session'] or 0, 2),
            },
            'bottleneck': diagnosis.bottleneck,
            'evidence': diagnosis.evidence,
            'confidence_score': diagnosis.confidence_score,
            'watch_metric': diagnosis.watch_metric,
            'top_recommendations': RecommendationSerializer(recommendations[:5], many=True).data,
            'next_recommendation': RecommendationSerializer(next_recommendation).data if next_recommendation else None,
            'recent_actions': ManualActionLogSerializer(recent_actions, many=True).data,
            'review_themes': ReviewThemeSerializer(review_themes, many=True).data,
            'latest_report': GrowthReportSerializer(latest_report).data if latest_report else None,
            'recent_reports': GrowthReportSerializer(app.growth_reports.all()[:5], many=True).data,
        }
    )


@api_view(['POST'])
def import_daily_metrics_view(request):
    app = get_object_or_404(AppProfile, pk=request.data['app'])
    uploaded = request.FILES.get('file')
    if not uploaded:
        return Response({'detail': 'CSV file is required.'}, status=status.HTTP_400_BAD_REQUEST)
    batch = import_daily_metrics(uploaded, app)
    AuditLog.objects.create(app=app, actor='user', event_type='import_daily_metrics', object_type='DataImportBatch', object_id=str(batch.id), summary='Imported daily metrics CSV')
    return Response(DataImportBatchSerializer(batch).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def import_reviews_view(request):
    app = get_object_or_404(AppProfile, pk=request.data['app'])
    uploaded = request.FILES.get('file')
    if not uploaded:
        return Response({'detail': 'CSV file is required.'}, status=status.HTTP_400_BAD_REQUEST)
    batch = import_reviews(uploaded, app)
    AuditLog.objects.create(app=app, actor='user', event_type='import_reviews', object_type='DataImportBatch', object_id=str(batch.id), summary='Imported reviews CSV')
    return Response(DataImportBatchSerializer(batch).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def listing_advisor_generate(request):
    app = get_object_or_404(AppProfile, pk=request.data['app'])
    listing_snapshot = app.listing_snapshots.order_by('-snapshot_date', '-created_at').first()
    ai = get_ai_provider()
    ai_result = ai.generate_listing_suggestions(app, listing_snapshot)
    return Response(
        {
            'app': AppProfileSerializer(app).data,
            'listing_snapshot': StoreListingSnapshotSerializer(listing_snapshot).data if listing_snapshot else None,
            'summary': ai_result.summary,
            'next_actions': ai_result.next_actions,
        }
    )


@api_view(['POST'])
def analyze_reviews_view(request):
    app = get_object_or_404(AppProfile, pk=request.data['app'])
    window_end = date.today()
    window_start = window_end - timedelta(days=30)
    reviews = app.reviews.filter(date__gte=window_start, date__lte=window_end).order_by('-date')
    analysis = ReviewAnalysisService().analyze(reviews)
    ReviewTheme.objects.filter(app=app, date_range_start=window_start, date_range_end=window_end).delete()
    created = [
        ReviewTheme.objects.create(
            app=app,
            date_range_start=window_start,
            date_range_end=window_end,
            category=item['category'],
            theme=item['theme'],
            count=item['count'],
            severity=item['severity'],
            examples_json=item['examples_json'],
            recommendation=item['recommendation'],
        )
        for item in analysis
    ]
    return Response(
        {
            'app': AppProfileSerializer(app).data,
            'window': {'start': window_start, 'end': window_end},
            'themes': ReviewThemeSerializer(created, many=True).data,
        }
    )

from .importers import import_android_vitals, import_ads

@api_view(['POST'])
def import_android_vitals_view(request):
    app = get_object_or_404(AppProfile, pk=request.data['app'])
    uploaded = request.FILES.get('file')
    if not uploaded:
        return Response({'detail': 'CSV file is required.'}, status=status.HTTP_400_BAD_REQUEST)
    batch = import_android_vitals(uploaded, app)
    AuditLog.objects.create(app=app, actor='user', event_type='import_android_vitals', object_type='DataImportBatch', object_id=str(batch.id), summary='Imported android vitals CSV')
    return Response(DataImportBatchSerializer(batch).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def import_ads_view(request):
    app = get_object_or_404(AppProfile, pk=request.data['app'])
    uploaded = request.FILES.get('file')
    if not uploaded:
        return Response({'detail': 'CSV file is required.'}, status=status.HTTP_400_BAD_REQUEST)
    batch = import_ads(uploaded, app)
    AuditLog.objects.create(app=app, actor='user', event_type='import_ads', object_type='DataImportBatch', object_id=str(batch.id), summary='Imported ads CSV')
    return Response(DataImportBatchSerializer(batch).data, status=status.HTTP_201_CREATED)
