import csv
from datetime import datetime
from io import TextIOWrapper

from .models import AppProfile, DailyMetric, DataImportBatch, ReviewItem, AndroidVitalsMetric, AdCampaignMetric


def _date(value):
    return datetime.strptime(value, '%Y-%m-%d').date()


def import_daily_metrics(file_obj, app: AppProfile):
    batch = DataImportBatch.objects.create(app=app, import_type='daily_metrics', source_filename=getattr(file_obj, 'name', ''), status='pending')
    try:
        wrapper = TextIOWrapper(file_obj.file, encoding='utf-8-sig') if hasattr(file_obj, 'file') else file_obj
        reader = csv.DictReader(wrapper)
        count = 0
        for row in reader:
            DailyMetric.objects.update_or_create(
                app=app,
                date=_date(row['date']),
                defaults={
                    'installs': int(row.get('installs') or 0),
                    'uninstalls': int(row.get('uninstalls') or 0),
                    'store_visitors': int(row.get('store_visitors') or 0),
                    'listing_conversion_rate': float(row['listing_conversion_rate']) if row.get('listing_conversion_rate') else None,
                    'active_users': int(row.get('active_users') or 0),
                    'day_1_retention': float(row['day_1_retention']) if row.get('day_1_retention') else None,
                    'day_7_retention': float(row['day_7_retention']) if row.get('day_7_retention') else None,
                    'average_session_length': float(row['average_session_length']) if row.get('average_session_length') else None,
                    'game_starts': int(row.get('game_starts') or 0),
                    'retry_count': int(row.get('retry_count') or 0),
                    'daily_challenge_opens': int(row.get('daily_challenge_opens') or 0),
                    'daily_challenge_completions': int(row.get('daily_challenge_completions') or 0),
                    'premium_clicks': int(row.get('premium_clicks') or 0),
                    'premium_purchases': int(row.get('premium_purchases') or 0),
                    'notes': row.get('notes', ''),
                    'import_batch': batch,
                },
            )
            count += 1
        batch.row_count = count
        batch.status = 'completed'
        batch.save()
        return batch
    except Exception as exc:
        batch.status = 'failed'
        batch.error_summary = str(exc)
        batch.save()
        raise


def import_reviews(file_obj, app: AppProfile):
    batch = DataImportBatch.objects.create(app=app, import_type='reviews', source_filename=getattr(file_obj, 'name', ''), status='pending')
    try:
        wrapper = TextIOWrapper(file_obj.file, encoding='utf-8-sig') if hasattr(file_obj, 'file') else file_obj
        reader = csv.DictReader(wrapper)
        count = 0
        for row in reader:
            ReviewItem.objects.create(
                app=app,
                date=_date(row['date']),
                rating=int(row.get('rating') or 0),
                reviewer_name=row.get('reviewer_name', ''),
                review_text=row.get('review_text', ''),
                device=row.get('device', ''),
                app_version=row.get('app_version', ''),
                language=row.get('language', 'en'),
                import_batch=batch,
            )
            count += 1
        batch.row_count = count
        batch.status = 'completed'
        batch.save()
        return batch
    except Exception as exc:
        batch.status = 'failed'
        batch.error_summary = str(exc)
        batch.save()
        raise

def import_android_vitals(file_obj, app: AppProfile):
    batch = DataImportBatch.objects.create(app=app, import_type='android_vitals', source_filename=getattr(file_obj, 'name', ''), status='pending')
    try:
        wrapper = TextIOWrapper(file_obj.file, encoding='utf-8-sig') if hasattr(file_obj, 'file') else file_obj
        reader = csv.DictReader(wrapper)
        count = 0
        for row in reader:
            AndroidVitalsMetric.objects.create(
                app=app,
                date=_date(row['date']),
                crash_rate=float(row['crash_rate']) if row.get('crash_rate') else None,
                anr_rate=float(row['anr_rate']) if row.get('anr_rate') else None,
                slow_rendering_rate=float(row['slow_rendering_rate']) if row.get('slow_rendering_rate') else None,
                excessive_wakeups=float(row['excessive_wakeups']) if row.get('excessive_wakeups') else None,
                affected_devices_json=row.get('affected_devices_json', '[]'),
                notes=row.get('notes', ''),
                import_batch=batch,
            )
            count += 1
        batch.row_count = count
        batch.status = 'completed'
        batch.save()
        return batch
    except Exception as exc:
        batch.status = 'failed'
        batch.error_summary = str(exc)
        batch.save()
        raise

def import_ads(file_obj, app: AppProfile):
    batch = DataImportBatch.objects.create(app=app, import_type='ads', source_filename=getattr(file_obj, 'name', ''), status='pending')
    try:
        wrapper = TextIOWrapper(file_obj.file, encoding='utf-8-sig') if hasattr(file_obj, 'file') else file_obj
        reader = csv.DictReader(wrapper)
        count = 0
        for row in reader:
            AdCampaignMetric.objects.create(
                app=app,
                date=_date(row['date']),
                campaign_name=row.get('campaign_name', ''),
                country_code=row.get('country_code', ''),
                spend=float(row.get('spend') or 0),
                impressions=int(row.get('impressions') or 0),
                clicks=int(row.get('clicks') or 0),
                installs=int(row.get('installs') or 0),
                cpi=float(row['cpi']) if row.get('cpi') else None,
                conversions=int(row.get('conversions') or 0),
                retention_d1=float(row['retention_d1']) if row.get('retention_d1') else None,
                retention_d7=float(row['retention_d7']) if row.get('retention_d7') else None,
                notes=row.get('notes', ''),
                import_batch=batch,
            )
            count += 1
        batch.row_count = count
        batch.status = 'completed'
        batch.save()
        return batch
    except Exception as exc:
        batch.status = 'failed'
        batch.error_summary = str(exc)
        batch.save()
        raise
