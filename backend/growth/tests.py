from datetime import date, timedelta

from django.test import TestCase

from .models import AppProfile, DailyMetric
from .services.diagnosis import BottleneckDiagnosisService
from .services.reports import GrowthReportService


class DiagnosisTests(TestCase):
    def test_store_conversion_problem_detected(self):
        app = AppProfile.objects.create(name='Test App', package_name='com.example.test')
        for i in range(5):
            DailyMetric.objects.create(
                app=app,
                date=date.today() - timedelta(days=i),
                installs=4,
                store_visitors=100,
                listing_conversion_rate=4.0,
            )
        result = BottleneckDiagnosisService().diagnose(app.daily_metrics.all())
        self.assertEqual(result.bottleneck, 'Store conversion problem')
        self.assertEqual(result.recommended_category, 'store_listing')


class ReportGenerationTests(TestCase):
    def test_report_generation_creates_safe_recommendation(self):
        app = AppProfile.objects.create(
            name='Test App',
            package_name='com.example.test',
            primary_positioning='Offline arcade sessions for short breaks.',
        )
        for i in range(7):
            DailyMetric.objects.create(
                app=app,
                date=date.today() - timedelta(days=i),
                installs=3,
                store_visitors=40,
                listing_conversion_rate=6.0,
                day_1_retention=18.0,
                day_7_retention=7.0,
            )

        report = GrowthReportService().generate(app, date.today() - timedelta(days=6), date.today())

        self.assertEqual(report.app_id, app.id)
        self.assertEqual(report.recommendations.count(), 1)
        recommendation = report.recommendations.first()
        self.assertEqual(recommendation.status, 'new')
        self.assertTrue(recommendation.priority)
        self.assertTrue(recommendation.why_this_matters)
