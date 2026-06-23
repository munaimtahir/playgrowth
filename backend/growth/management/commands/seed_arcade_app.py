from django.core.management.base import BaseCommand
from growth.models import AppProfile

class Command(BaseCommand):
    help = 'Seeds the Offline Mini Arcade app profile idempotently'

    def handle(self, *args, **options):
        app, created = AppProfile.objects.update_or_create(
            package_name='com.example.offlineminiarcade',
            defaults={
                'name': 'Offline Mini Arcade',
                'play_store_url': 'https://play.google.com/store/apps/details?id=com.example.offlineminiarcade',
                'category': 'Arcade',
                'app_type': 'Game',
                'primary_positioning': 'Lightweight offline-first mini arcade with Pulse Orbit, Lane Drift, and Stack Drop. Built for quick sessions and low-end Android devices.',
                'target_countries': 'Pakistan, India, Philippines, Indonesia, United States, United Kingdom',
                'monetization_model': 'Free / non-aggressive monetization',
                'current_version': '1.0.0'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Offline Mini Arcade'))
        else:
            self.stdout.write(self.style.SUCCESS('Successfully updated Offline Mini Arcade'))
