from datetime import date, timedelta
from django.test import TestCase
from .models import AppProfile, DailyMetric
from .services.diagnosis import BottleneckDiagnosisService


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
