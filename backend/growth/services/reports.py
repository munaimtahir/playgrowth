from .ai import get_ai_provider
from .diagnosis import BottleneckDiagnosisService
from .safety import normalize_recommendation
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
        created = []
        for item in ai_result.next_actions:
            normalized = normalize_recommendation(item)
            recommendation = Recommendation.objects.create(
                app=app,
                source_report=report,
                category=normalized.category,
                title=normalized.title,
                priority=normalized.priority,
                diagnosis=normalized.diagnosis,
                evidence_json=normalized.evidence,
                suggested_human_action=normalized.suggested_human_action,
                copyable_text=normalized.copyable_text,
                do_not_do_yet=normalized.do_not_do_yet,
                expected_impact=normalized.why_this_matters,
                why_this_matters=normalized.why_this_matters,
                risk_level=normalized.risk_level,
                effort_level=normalized.effort_level,
                confidence_score=normalized.confidence_score,
                watch_metric=normalized.watch_metric,
            )
            created.append(recommendation)

        if not created:
            fallback = normalize_recommendation(
                {
                    'category': 'experiment',
                    'title': 'Define one manual experiment',
                    'priority': 'medium',
                    'diagnosis': 'No single severe bottleneck was detected.',
                    'evidence': ['Metrics look stable enough to keep observing.'],
                    'suggested_human_action': 'Choose one small manual experiment, document it, and track the result for 7 to 14 days.',
                    'why_this_matters': 'A controlled experiment creates a measurable next step instead of passive observation.',
                    'risk_level': 'low',
                    'effort_level': 'medium',
                    'confidence_score': 0.55,
                    'watch_metric': 'installs, conversion, retention, reviews',
                }
            )
            Recommendation.objects.create(
                app=app,
                source_report=report,
                category=fallback.category,
                title=fallback.title,
                priority=fallback.priority,
                diagnosis=fallback.diagnosis,
                evidence_json=fallback.evidence,
                suggested_human_action=fallback.suggested_human_action,
                copyable_text=fallback.copyable_text,
                do_not_do_yet=fallback.do_not_do_yet,
                expected_impact=fallback.why_this_matters,
                why_this_matters=fallback.why_this_matters,
                risk_level=fallback.risk_level,
                effort_level=fallback.effort_level,
                confidence_score=fallback.confidence_score,
                watch_metric=fallback.watch_metric,
            )
        return report
