from datetime import date, timedelta
from django.core.management.base import BaseCommand
from growth.models import AppProfile, DailyMetric, ReviewItem, StoreListingSnapshot


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
        self.stdout.write(self.style.SUCCESS('Seeded Offline Mini Arcade demo data.'))
