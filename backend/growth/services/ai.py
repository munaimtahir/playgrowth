from dataclasses import dataclass

from .safety import normalize_category, normalize_recommendation


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
        action = normalize_recommendation(
            {
                'category': normalize_category(diagnosis.recommended_category),
                'title': self._title_for(diagnosis.bottleneck),
                'priority': self._priority_for(diagnosis.bottleneck),
                'diagnosis': diagnosis.bottleneck,
                'evidence': diagnosis.evidence,
                'suggested_human_action': self._action_for(diagnosis.bottleneck, app),
                'copyable_text': self._copy_for(diagnosis.bottleneck, app),
                'do_not_do_yet': self._avoid_for(diagnosis.bottleneck),
                'why_this_matters': self._why_for(diagnosis.bottleneck, diagnosis.watch_metric),
                'risk_level': self._risk_for(diagnosis.bottleneck),
                'effort_level': self._effort_for(diagnosis.bottleneck),
                'confidence_score': diagnosis.confidence_score,
                'watch_metric': diagnosis.watch_metric,
            }
        )
        return AIResult(
            summary=(
                f'{app.name}: {diagnosis.bottleneck}. '
                'This copilot only recommends manual changes; it does not touch Play Console, ads, or releases.'
            ),
            next_actions=[action.__dict__],
        )

    def generate_listing_suggestions(self, app, listing_snapshot):
        base_copy = [
            'Lightweight offline arcade for quick sessions.',
            'Three small games: Pulse Orbit, Lane Drift, and Stack Drop.',
            'Built for low-end Android phones and short breaks.',
        ]
        suggestions = [
            normalize_recommendation(
                {
                    'category': 'store_listing',
                    'title': 'Clarify the offline quick-session value',
                    'priority': 'high',
                    'diagnosis': 'The listing should explain the core value within the first few seconds.',
                    'evidence': [f'App positioning: {app.primary_positioning or "offline-first arcade games"}'],
                    'suggested_human_action': 'Manually test a clearer short description in Play Console or a store listing experiment.',
                    'copyable_text': base_copy[0],
                    'do_not_do_yet': 'Do not keyword-stuff arcade or offline terms repeatedly.',
                    'why_this_matters': 'Clear positioning improves the chance that the right users tap install.',
                    'risk_level': 'low',
                    'effort_level': 'low',
                    'confidence_score': 0.7,
                    'watch_metric': 'listing_conversion_rate',
                }
            ),
            normalize_recommendation(
                {
                    'category': 'screenshots',
                    'title': 'Make the first screenshot do more work',
                    'priority': 'medium',
                    'diagnosis': 'The first screenshot should explain the game loop and offline nature without clutter.',
                    'evidence': ['Mobile store visitors scan screenshots before reading the full description.'],
                    'suggested_human_action': 'Manually add one short caption per screenshot and keep the first one focused on the core gameplay promise.',
                    'copyable_text': 'Quick arcade sessions. Offline. Low-end friendly.',
                    'do_not_do_yet': 'Do not add claims you cannot prove with gameplay.',
                    'why_this_matters': 'Improving the first screenshot can raise conversion without changing traffic quality.',
                    'risk_level': 'low',
                    'effort_level': 'medium',
                    'confidence_score': 0.65,
                    'watch_metric': 'listing_conversion_rate and screenshot click-through',
                }
            ),
        ]
        return AIResult(
            summary='Listing drafts generated as copyable suggestions only. Review them manually before any Play Console change.',
            next_actions=[item.__dict__ for item in suggestions],
        )

    def _title_for(self, bottleneck):
        text = bottleneck.lower()
        if 'conversion' in text:
            return 'Improve store conversion'
        if 'discovery' in text:
            return 'Clarify discovery signals'
        if 'retention' in text:
            return 'Reduce early churn'
        if 'quality' in text or 'stability' in text:
            return 'Fix product stability'
        if 'ads' in text:
            return 'Improve paid acquisition efficiency'
        if 'review' in text:
            return 'Resolve repeated review themes'
        return 'Run a controlled manual experiment'

    def _priority_for(self, bottleneck):
        text = bottleneck.lower()
        if any(term in text for term in ['quality', 'stability', 'crash']):
            return 'high'
        if any(term in text for term in ['conversion', 'retention', 'ads', 'review']):
            return 'high'
        return 'medium'

    def _action_for(self, bottleneck, app):
        text = bottleneck.lower()
        if 'conversion' in text:
            return 'Manually improve the first screenshot caption and short description to communicate offline, lightweight, quick-session value.'
        if 'discovery' in text:
            return 'Manually review title, short description, and first paragraph for clear ASO without keyword stuffing.'
        if 'retention' in text:
            return 'Review first-run gameplay clarity, difficulty pacing, and retry loop before increasing traffic.'
        if 'quality' in text or 'stability' in text:
            return 'Fix crashes and ANRs before changing listing or scaling ads.'
        if 'ads' in text:
            return 'Tighten targeting and creative manually, then watch CPI and retention before spending more.'
        if 'review' in text:
            return 'Group the recurring complaints, fix the product issue, and only then consider a manual reply draft.'
        return 'Choose one small manual experiment, document it, and track the result for 7 to 14 days.'

    def _copy_for(self, bottleneck, app):
        text = bottleneck.lower()
        if 'conversion' in text or 'discovery' in text:
            return 'Lightweight offline arcade for quick sessions. Three games: Pulse Orbit, Lane Drift, and Stack Drop.'
        if 'retention' in text:
            return 'Short, replayable arcade rounds built for low-end Android phones.'
        if 'quality' in text or 'stability' in text:
            return 'Fix stability first, then revisit store messaging.'
        return app.primary_positioning or 'Manual growth analysis only.'

    def _avoid_for(self, bottleneck):
        text = bottleneck.lower()
        if 'conversion' in text or 'discovery' in text:
            return 'Do not increase ads budget until store conversion improves.'
        if 'quality' in text or 'stability' in text:
            return 'Do not promote aggressively until crash and ANR issues are fixed.'
        if 'review' in text:
            return 'Do not fabricate reviews, manipulate ratings, or script deceptive responses.'
        return 'Do not make multiple public changes at once without logging them.'

    def _why_for(self, bottleneck, watch_metric):
        text = bottleneck.lower()
        if 'conversion' in text:
            return 'More store visitors are already available, so the page itself is limiting installs.'
        if 'discovery' in text:
            return 'If visitors are low, better traffic quality starts with clearer store positioning.'
        if 'retention' in text:
            return 'Better early retention makes paid or organic traffic more valuable.'
        if 'quality' in text or 'stability' in text:
            return 'Crash and ANR issues reduce session quality and can suppress store performance.'
        if 'review' in text:
            return 'Recurring complaint themes point to product friction that manual fixes can address.'
        return f'Watching {watch_metric} will tell you whether the manual experiment changed the bottleneck.'

    def _risk_for(self, bottleneck):
        text = bottleneck.lower()
        if 'quality' in text or 'stability' in text:
            return 'high'
        if 'ads' in text:
            return 'medium'
        return 'low'

    def _effort_for(self, bottleneck):
        text = bottleneck.lower()
        if 'quality' in text or 'stability' in text:
            return 'high'
        if 'conversion' in text or 'discovery' in text:
            return 'medium'
        return 'medium'


def get_ai_provider():
    return MockAIProvider()
