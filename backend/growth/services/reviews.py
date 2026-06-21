from __future__ import annotations

from collections import Counter

from .safety import ensure_safe_text


class ReviewAnalysisService:
    KEYWORDS = {
        'controls': ['control', 'touch', 'button', 'swipe', 'clunky'],
        'difficulty': ['hard', 'easy', 'difficulty', 'impossible', 'challenge'],
        'stability': ['crash', 'freeze', 'lag', 'anr', 'slow'],
        'offline': ['offline', 'internet', 'network', 'connection'],
        'content': ['more levels', 'more games', 'content', 'boring', 'repeat'],
        'ads': ['ad', 'ads', 'rewarded', 'interstitial'],
    }

    def analyze(self, reviews):
        reviews = list(reviews)
        themes = []
        if not reviews:
            return themes

        counter = Counter()
        examples = {name: [] for name in self.KEYWORDS}
        for review in reviews:
            text = (review.review_text or '').lower()
            for theme, terms in self.KEYWORDS.items():
                if any(term in text for term in terms):
                    counter[theme] += 1
                    if len(examples[theme]) < 3:
                        examples[theme].append(review.review_text)

        for theme, count in counter.most_common():
            themes.append(
                {
                    'category': self._category_for(theme),
                    'theme': ensure_safe_text(self._theme_label(theme)),
                    'count': count,
                    'severity': self._severity_for(count, reviews),
                    'examples_json': examples[theme],
                    'recommendation': self._recommendation_for(theme),
                }
            )
        return themes

    def _category_for(self, theme):
        return {
            'controls': 'product',
            'difficulty': 'retention',
            'stability': 'crashes',
            'offline': 'product',
            'content': 'experiment',
            'ads': 'ads',
        }.get(theme, 'reviews')

    def _theme_label(self, theme):
        return {
            'controls': 'Controls feel awkward on some devices',
            'difficulty': 'Players want a better difficulty curve',
            'stability': 'Stability complaints appear in reviews',
            'offline': 'Offline behavior is mentioned frequently',
            'content': 'Users want more content or variety',
            'ads': 'Reviewers mention ads',
        }.get(theme, theme.replace('_', ' '))

    def _severity_for(self, count, reviews):
        if count >= max(4, len(reviews) // 3):
            return 'high'
        if count >= 2:
            return 'medium'
        return 'low'

    def _recommendation_for(self, theme):
        return {
            'controls': 'Manually test larger controls or clearer touch affordances, then check ratings on the next import.',
            'difficulty': 'Adjust early-game pacing before changing traffic or store copy.',
            'stability': 'Fix crashes or ANRs before any growth push.',
            'offline': 'Clarify the offline promise in the listing and onboarding text.',
            'content': 'Plan one content-focused experiment and measure retention before scaling traffic.',
            'ads': 'Keep monetization light and avoid aggressive ad placement changes.',
        }.get(theme, 'Review the recurring theme manually and log the outcome after the fix.')
