import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'games.settings')

app = Celery('games', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'email-reminder-everyday': {
        'task': 'authentication.tasks.send_weekly_reminder_confirm_email',
        'schedule': crontab(day_of_week='*', hour=9, minute=30),
    },
}
app.conf.timezone = 'Europe/Kiev'
