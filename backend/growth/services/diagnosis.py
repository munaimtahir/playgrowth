from dataclasses import dataclass
from statistics import mean


@dataclass
class DiagnosisResult:
    bottleneck: str
    evidence: list[str]
    confidence_score: float
    watch_metric: str
    recommended_category: str


class BottleneckDiagnosisService:
    """Deterministic growth diagnosis before AI wording is added."""

    def diagnose(self, metrics, vitals=None, ads=None, reviews=None) -> DiagnosisResult:
        metrics = list(metrics)
        vitals = list(vitals or [])
        ads = list(ads or [])
        reviews = list(reviews or [])

        if len(metrics) < 3:
            return DiagnosisResult(
                bottleneck='Insufficient data',
                evidence=['Fewer than 3 daily metric rows are available.'],
                confidence_score=0.35,
                watch_metric='Add at least 7 days of daily metrics',
                recommended_category='measurement',
            )

        visitors = [m.store_visitors for m in metrics]
        installs = [m.installs for m in metrics]
        conversions = [m.listing_conversion_rate for m in metrics if m.listing_conversion_rate is not None]
        d1 = [m.day_1_retention for m in metrics if m.day_1_retention is not None]

        avg_visitors = mean(visitors) if visitors else 0
        avg_installs = mean(installs) if installs else 0
        avg_conversion = mean(conversions) if conversions else 0
        avg_d1 = mean(d1) if d1 else None

        high_crash = any((v.crash_rate or 0) >= 1.0 or (v.anr_rate or 0) >= 0.5 for v in vitals)
        low_rating_reviews = [r for r in reviews if r.rating and r.rating <= 3]
        ad_spend = sum(a.spend for a in ads)
        ad_installs = sum(a.installs for a in ads)
        avg_cpi = (ad_spend / ad_installs) if ad_spend and ad_installs else None

        if high_crash:
            return DiagnosisResult(
                bottleneck='Quality/stability problem',
                evidence=['Crash or ANR signal is above safe threshold.'],
                confidence_score=0.82,
                watch_metric='crash_rate and anr_rate',
                recommended_category='crashes',
            )

        if avg_visitors < 20 and avg_installs < 3:
            return DiagnosisResult(
                bottleneck='Discovery problem',
                evidence=[f'Average daily visitors are low ({avg_visitors:.1f}).'],
                confidence_score=0.72,
                watch_metric='store_visitors',
                recommended_category='store_listing',
            )

        if avg_visitors >= 20 and avg_conversion and avg_conversion < 10:
            return DiagnosisResult(
                bottleneck='Store conversion problem',
                evidence=[f'Visitors exist but average conversion is low ({avg_conversion:.1f}%).'],
                confidence_score=0.78,
                watch_metric='listing_conversion_rate',
                recommended_category='store_listing',
            )

        if avg_d1 is not None and avg_d1 < 20:
            return DiagnosisResult(
                bottleneck='Retention/onboarding problem',
                evidence=[f'Day-1 retention is weak ({avg_d1:.1f}%).'],
                confidence_score=0.74,
                watch_metric='day_1_retention',
                recommended_category='retention',
            )

        if len(low_rating_reviews) >= 3:
            return DiagnosisResult(
                bottleneck='Review/theme problem',
                evidence=[f'{len(low_rating_reviews)} recent reviews are rated 3 stars or lower.'],
                confidence_score=0.7,
                watch_metric='review rating and repeated themes',
                recommended_category='reviews',
            )

        if avg_cpi is not None and avg_cpi > 1.0 and (avg_conversion or 0) < 15:
            return DiagnosisResult(
                bottleneck='Ads efficiency problem',
                evidence=[f'Ads CPI is high relative to current conversion (CPI {avg_cpi:.2f}).'],
                confidence_score=0.67,
                watch_metric='CPI and listing conversion rate',
                recommended_category='ads',
            )

        return DiagnosisResult(
            bottleneck='No single severe bottleneck detected',
            evidence=['Available metrics do not show one dominant issue. Continue controlled observation.'],
            confidence_score=0.55,
            watch_metric='installs, conversion, retention, reviews',
            recommended_category='experiment',
        )
