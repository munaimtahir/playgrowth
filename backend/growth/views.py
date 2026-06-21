from datetime import date, timedelta

from django.db.models import Avg, Sum
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
from .services.diagnosis import BottleneckDiagnosisService
from .services.reports import GrowthReportService


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
        app = AppProfile.objects.get(pk=request.data['app'])
        period_end = date.fromisoformat(request.data.get('period_end')) if request.data.get('period_end') else date.today()
        period_start = date.fromisoformat(request.data.get('period_start')) if request.data.get('period_start') else period_end - timedelta(days=7)
        report_type = request.data.get('report_type', 'weekly')
        report = GrowthReportService().generate(app, period_start, period_end, report_type=report_type)
        return Response(GrowthReportSerializer(report).data, status=status.HTTP_201_CREATED)


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.select_related('app', 'source_report').all()
    serializer_class = RecommendationSerializer
    filterset_fields = ['app', 'status', 'category', 'risk_level', 'effort_level']

    def _set_status(self, request, pk, next_status, timestamp_field=None):
        rec = self.get_object()
        rec.status = next_status
        if timestamp_field:
            setattr(rec, timestamp_field, timezone.now())
        rec.save()
        AuditLog.objects.create(app=rec.app, actor='user', event_type=f'recommendation_{next_status}', object_type='Recommendation', object_id=str(rec.id), summary=rec.title)
        return Response(self.get_serializer(rec).data)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        return self._set_status(request, pk, 'accepted_to_try', 'accepted_at')

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        return self._set_status(request, pk, 'rejected')

    @action(detail=True, methods=['post'], url_path='mark-implemented')
    def mark_implemented(self, request, pk=None):
        return self._set_status(request, pk, 'manually_implemented', 'implemented_at')

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        return self._set_status(request, pk, 'closed', 'closed_at')


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
def dashboard_summary(request):
    app = AppProfile.objects.get(pk=request.query_params['app'])
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    metrics = app.daily_metrics.all()
    if start:
        metrics = metrics.filter(date__gte=start)
    if end:
        metrics = metrics.filter(date__lte=end)
    vitals = app.vitals.all()
    ads = app.ads.all()
    reviews = app.reviews.all()
    aggregate = metrics.aggregate(
        installs=Sum('installs'),
        visitors=Sum('store_visitors'),
        conversion=Avg('listing_conversion_rate'),
        d1=Avg('day_1_retention'),
        d7=Avg('day_7_retention'),
    )
    diagnosis = BottleneckDiagnosisService().diagnose(metrics.order_by('date'), vitals=vitals, ads=ads, reviews=reviews)
    return Response({
        'app': AppProfileSerializer(app).data,
        'kpis': {
            'installs': aggregate['installs'] or 0,
            'store_visitors': aggregate['visitors'] or 0,
            'conversion_rate': round(aggregate['conversion'] or 0, 2),
            'day_1_retention': round(aggregate['d1'] or 0, 2),
            'day_7_retention': round(aggregate['d7'] or 0, 2),
        },
        'bottleneck': diagnosis.bottleneck,
        'evidence': diagnosis.evidence,
        'confidence_score': diagnosis.confidence_score,
        'top_recommendations': RecommendationSerializer(app.recommendations.all()[:5], many=True).data,
        'recent_actions': ManualActionLogSerializer(app.manual_actions.all()[:5], many=True).data,
    })


@api_view(['POST'])
def import_daily_metrics_view(request):
    app = AppProfile.objects.get(pk=request.data['app'])
    batch = import_daily_metrics(request.FILES['file'], app)
    return Response(DataImportBatchSerializer(batch).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def import_reviews_view(request):
    app = AppProfile.objects.get(pk=request.data['app'])
    batch = import_reviews(request.FILES['file'], app)
    return Response(DataImportBatchSerializer(batch).data, status=status.HTTP_201_CREATED)
