import csv
from datetime import datetime
from io import TextIOWrapper

from .models import AppProfile, DailyMetric, DataImportBatch, ReviewItem


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
