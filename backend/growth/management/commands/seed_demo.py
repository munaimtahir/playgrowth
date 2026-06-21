from datetime import date, timedelta
from django.core.management.base import BaseCommand
from growth.models import AdCampaignMetric, AndroidVitalsMetric, AppProfile, DailyMetric, Experiment, ManualActionLog, ReviewItem, ReviewTheme, StoreListingSnapshot
from growth.services.reports import GrowthReportService
from growth.services.reviews import ReviewAnalysisService


class Command(BaseCommand):
    help = 'Seed demo data for Offline Mini Arcade.'

    def handle(self, *args, **options):
        app, _ = AppProfile.objects.update_or_create(
            package_name='com.example.offlineminiarcade',
            defaults={
                'name': 'Offline Mini Arcade',
                'play_store_url': 'https://play.google.com/store/apps/details?id=com.example.offlineminiarcade',
                'category': 'Arcade',
                'app_type': 'Game',
                'primary_positioning': 'Lightweight offline-first mini arcade with Pulse Orbit, Lane Drift, and Stack Drop. Built for quick sessions and low-end Android devices.',
                'target_countries': 'Pakistan, India, Philippines, Indonesia, United States, United Kingdom',
                'monetization_model': 'Free / non-aggressive monetization',
                'current_version': '1.0.0',
            },
        )
        today = date.today()
        for i in range(10):
            d = today - timedelta(days=9 - i)
            DailyMetric.objects.update_or_create(
                app=app,
                date=d,
                defaults={
                    'installs': 4 + i,
                    'uninstalls': 1,
                    'store_visitors': 80 + (i * 10),
                    'listing_conversion_rate': 5.0 + (i * 0.4),
                    'active_users': 12 + i,
                    'day_1_retention': 18 + (i * 0.7),
                    'day_7_retention': 7 + (i * 0.2),
                    'average_session_length': 120 + (i * 4),
                    'game_starts': 30 + (i * 5),
                    'retry_count': 15 + (i * 2),
                    'notes': 'Demo metric row',
                },
            )
        StoreListingSnapshot.objects.get_or_create(
            app=app,
            snapshot_date=today,
            app_title='Offline Mini Arcade',
            defaults={
                'short_description': 'Play quick arcade games offline.',
                'full_description': 'Pulse Orbit, Lane Drift, and Stack Drop in one lightweight arcade app.',
                'screenshot_notes': 'Current screenshots show all three games but may need clearer captions.',
                'feature_graphic_notes': 'Should communicate offline, lightweight, quick sessions.',
                'status': 'current',
            },
        )
        ReviewItem.objects.get_or_create(app=app, date=today, reviewer_name='Demo User A', review_text='Nice small games and works offline.', defaults={'rating': 5, 'language': 'en'})
        ReviewItem.objects.get_or_create(app=app, date=today, reviewer_name='Demo User B', review_text='Stack game controls feel a little cramped on my phone.', defaults={'rating': 3, 'language': 'en'})
        review_themes = ReviewAnalysisService().analyze(app.reviews.all())
        ReviewTheme.objects.filter(app=app).delete()
        for theme in review_themes:
            ReviewTheme.objects.create(
                app=app,
                date_range_start=today - timedelta(days=30),
                date_range_end=today,
                category=theme['category'],
                theme=theme['theme'],
                count=theme['count'],
                severity=theme['severity'],
                examples_json=theme['examples_json'],
                recommendation=theme['recommendation'],
            )
        AndroidVitalsMetric.objects.update_or_create(
            app=app,
            date=today - timedelta(days=1),
            defaults={'crash_rate': 0.18, 'anr_rate': 0.12, 'slow_rendering_rate': 0.4, 'notes': 'Demo vitals are healthy.'},
        )
        AdCampaignMetric.objects.update_or_create(
            app=app,
            date=today - timedelta(days=1),
            campaign_name='Demo Arcade Install Campaign',
            defaults={'country_code': 'PK', 'spend': 12.5, 'impressions': 1200, 'clicks': 74, 'installs': 18, 'cpi': 0.69, 'conversions': 4},
        )
        Experiment.objects.update_or_create(
            app=app,
            name='Test clearer first screenshot caption',
            defaults={
                'hypothesis': 'If the first screenshot explains offline quick sessions, then store conversion will improve.',
                'area': 'screenshots',
                'variant_a': 'Current screenshot caption',
                'variant_b': 'Offline quick-session promise',
                'primary_metric': 'listing_conversion_rate',
                'secondary_metric': 'store_visitors',
                'status': 'planned',
                'minimum_duration_days': 7,
                'minimum_sample_size': 100,
            },
        )
        ManualActionLog.objects.update_or_create(
            app=app,
            action_date=today - timedelta(days=2),
            action_type='screenshot_change',
            title='Updated screenshot captions locally',
            defaults={
                'description': 'Tested a clearer first screenshot message before any Play Console update.',
                'changed_location': 'Design draft only',
                'expected_metric': 'listing_conversion_rate',
            },
        )[0]
        GrowthReportService().generate(app, today - timedelta(days=7), today, report_type='weekly')
        self.stdout.write(self.style.SUCCESS('Seeded Offline Mini Arcade demo data.'))
