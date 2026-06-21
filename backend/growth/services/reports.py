from .ai import get_ai_provider
from .diagnosis import BottleneckDiagnosisService
from ..models import GrowthReport, Recommendation


class GrowthReportService:
    def generate(self, app, period_start, period_end, report_type='weekly'):
        metrics = app.daily_metrics.filter(date__gte=period_start, date__lte=period_end).order_by('date')
        vitals = app.vitals.filter(date__gte=period_start, date__lte=period_end)
        ads = app.ads.filter(date__gte=period_start, date__lte=period_end)
        reviews = app.reviews.filter(date__gte=period_start, date__lte=period_end)
        diagnosis = BottleneckDiagnosisService().diagnose(metrics, vitals=vitals, ads=ads, reviews=reviews)
        ai = get_ai_provider()
        ai_result = ai.generate_growth_report(app, diagnosis, metrics)
        report = GrowthReport.objects.create(
            app=app,
            period_start=period_start,
            period_end=period_end,
            report_type=report_type,
            summary=ai_result.summary,
            bottleneck=diagnosis.bottleneck,
            evidence_json=diagnosis.evidence,
            next_actions_json=ai_result.next_actions,
            confidence_score=diagnosis.confidence_score,
            ai_provider=ai.name,
        )
        for item in ai_result.next_actions:
            Recommendation.objects.create(
                app=app,
                source_report=report,
                category=item.get('category', 'general'),
                title=item.get('title', 'Recommendation'),
                diagnosis=item.get('diagnosis', ''),
                evidence_json=item.get('evidence', []),
                suggested_human_action=item.get('suggested_human_action', ''),
                copyable_text=item.get('copyable_text', ''),
                do_not_do_yet=item.get('do_not_do_yet', ''),
                expected_impact=item.get('expected_impact', ''),
                risk_level=item.get('risk_level', 'low'),
                effort_level=item.get('effort_level', 'low'),
                confidence_score=item.get('confidence_score', 0),
                watch_metric=item.get('watch_metric', ''),
            )
        return report
