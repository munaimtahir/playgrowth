from datetime import date, timedelta
from celery import shared_task
from .models import AppProfile
from .services.reports import GrowthReportService


@shared_task
def generate_weekly_reports():
    period_end = date.today()
    period_start = period_end - timedelta(days=7)
    for app in AppProfile.objects.all():
        GrowthReportService().generate(app, period_start, period_end, report_type='weekly')
