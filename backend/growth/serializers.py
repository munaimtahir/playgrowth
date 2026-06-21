from rest_framework import serializers
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


class AppProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppProfile
        fields = '__all__'


class DataImportBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataImportBatch
        fields = '__all__'


class DailyMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMetric
        fields = '__all__'


class CountryMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMetric
        fields = '__all__'


class StoreListingSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreListingSnapshot
        fields = '__all__'


class ReviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewItem
        fields = '__all__'


class ReviewThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTheme
        fields = '__all__'


class AndroidVitalsMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = AndroidVitalsMetric
        fields = '__all__'


class AdCampaignMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdCampaignMetric
        fields = '__all__'


class GrowthReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthReport
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'


class ManualActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualActionLog
        fields = '__all__'


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
