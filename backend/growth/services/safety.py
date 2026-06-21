from __future__ import annotations

from dataclasses import dataclass


FORBIDDEN_PHRASES = [
    'fake review',
    'fake reviews',
    'fake install',
    'fake installs',
    'keyword stuffing',
    'misleading claim',
    'misleading claims',
    'review manipulation',
    'dark pattern',
    'aggressive monetization',
    'buy reviews',
    'buy installs',
]

ALLOWED_CATEGORIES = {
    'store_listing',
    'screenshots',
    'feature_graphic',
    'reviews',
    'retention',
    'crashes',
    'ads',
    'product',
    'experiment',
    'measurement',
}

ALLOWED_PRIORITIES = {'high', 'medium', 'low'}
ALLOWED_RISK_LEVELS = {'high', 'medium', 'low'}
ALLOWED_EFFORT_LEVELS = {'high', 'medium', 'low'}


def ensure_safe_text(text: str) -> str:
    normalized = text.strip()
    lowered = normalized.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lowered:
            raise ValueError(f'Unsafe recommendation text contains forbidden phrase: {phrase}')
    return normalized


def normalize_category(category: str) -> str:
    value = (category or 'experiment').strip()
    return value if value in ALLOWED_CATEGORIES else 'experiment'


def normalize_level(value: str, allowed: set[str], default: str) -> str:
    cleaned = (value or default).strip().lower()
    return cleaned if cleaned in allowed else default


@dataclass(frozen=True)
class SafeRecommendation:
    category: str
    title: str
    priority: str
    diagnosis: str
    evidence: list[str]
    suggested_human_action: str
    copyable_text: str
    do_not_do_yet: str
    why_this_matters: str
    risk_level: str
    effort_level: str
    confidence_score: float
    watch_metric: str


def normalize_recommendation(payload: dict) -> SafeRecommendation:
    return SafeRecommendation(
        category=normalize_category(payload.get('category', 'experiment')),
        title=ensure_safe_text(payload.get('title', 'Recommendation')),
        priority=normalize_level(payload.get('priority', 'medium'), ALLOWED_PRIORITIES, 'medium'),
        diagnosis=ensure_safe_text(payload.get('diagnosis', '')),
        evidence=[ensure_safe_text(str(item)) for item in payload.get('evidence', [])],
        suggested_human_action=ensure_safe_text(payload.get('suggested_human_action', '')),
        copyable_text=ensure_safe_text(payload.get('copyable_text', '')) if payload.get('copyable_text') else '',
        do_not_do_yet=ensure_safe_text(payload.get('do_not_do_yet', '')) if payload.get('do_not_do_yet') else '',
        why_this_matters=ensure_safe_text(payload.get('why_this_matters', '')) if payload.get('why_this_matters') else '',
        risk_level=normalize_level(payload.get('risk_level', 'low'), ALLOWED_RISK_LEVELS, 'low'),
        effort_level=normalize_level(payload.get('effort_level', 'low'), ALLOWED_EFFORT_LEVELS, 'low'),
        confidence_score=float(payload.get('confidence_score', 0)),
        watch_metric=ensure_safe_text(payload.get('watch_metric', '')) if payload.get('watch_metric') else '',
    )
