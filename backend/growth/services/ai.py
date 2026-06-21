from dataclasses import dataclass


@dataclass
class AIResult:
    summary: str
    next_actions: list[dict]


class BaseAIProvider:
    name = 'base'

    def generate_growth_report(self, app, diagnosis, metrics):
        raise NotImplementedError

    def generate_listing_suggestions(self, app, listing_snapshot):
        raise NotImplementedError


class MockAIProvider(BaseAIProvider):
    name = 'mock'

    def generate_growth_report(self, app, diagnosis, metrics):
        action = {
            'category': diagnosis.recommended_category,
            'title': f'Address {diagnosis.bottleneck.lower()}',
            'diagnosis': diagnosis.bottleneck,
            'evidence': diagnosis.evidence,
            'suggested_human_action': self._action_for(diagnosis.bottleneck, app),
            'copyable_text': self._copy_for(diagnosis.bottleneck),
            'do_not_do_yet': self._avoid_for(diagnosis.bottleneck),
            'expected_impact': f'Improvement in {diagnosis.watch_metric}.',
            'risk_level': 'low',
            'effort_level': 'low' if diagnosis.recommended_category == 'store_listing' else 'medium',
            'confidence_score': diagnosis.confidence_score,
            'watch_metric': diagnosis.watch_metric,
        }
        return AIResult(
            summary=f'{app.name}: {diagnosis.bottleneck}. The safest next step is a manual, measurable change rather than automation.',
            next_actions=[action],
        )

    def generate_listing_suggestions(self, app, listing_snapshot):
        base = '3 quick arcade games. Works offline. Lightweight fun for short breaks.'
        return AIResult(
            summary='Listing suggestions generated as copyable drafts only. Manually review and implement in Play Console.',
            next_actions=[
                {
                    'category': 'store_listing',
                    'title': 'Clarify offline quick-session value',
                    'diagnosis': 'The listing should explain the core value within the first few seconds.',
                    'evidence': ['App positioning says offline-first, lightweight, quick arcade sessions.'],
                    'suggested_human_action': 'Manually test a clearer short description in Play Console or a store listing experiment.',
                    'copyable_text': base,
                    'do_not_do_yet': 'Do not keyword-stuff arcade/game/offline terms repeatedly.',
                    'expected_impact': 'Potential improvement in listing conversion rate.',
                    'risk_level': 'low',
                    'effort_level': 'low',
                    'confidence_score': 0.65,
                    'watch_metric': 'listing_conversion_rate',
                }
            ],
        )

    def _action_for(self, bottleneck, app):
        if 'conversion' in bottleneck.lower():
            return 'Manually improve the first screenshot caption and short description to communicate offline, lightweight, quick-session value.'
        if 'discovery' in bottleneck.lower():
            return 'Manually review title, short description, and first paragraph for clear ASO without keyword stuffing.'
        if 'retention' in bottleneck.lower():
            return 'Review first-run gameplay clarity and result/retry loop before increasing traffic.'
        if 'quality' in bottleneck.lower():
            return 'Fix stability issues before changing listing or scaling ads.'
        return 'Choose one small manual experiment and track the result for 7–14 days.'

    def _copy_for(self, bottleneck):
        if 'conversion' in bottleneck.lower() or 'discovery' in bottleneck.lower():
            return '3 quick arcade games. Works offline. Lightweight fun for short breaks.'
        return ''

    def _avoid_for(self, bottleneck):
        if 'conversion' in bottleneck.lower():
            return 'Do not increase ads budget until store conversion improves.'
        if 'quality' in bottleneck.lower():
            return 'Do not promote aggressively until crash/ANR issues are fixed.'
        return 'Do not make multiple listing changes at once without logging them.'


def get_ai_provider():
    return MockAIProvider()
