import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookAppAPI.settings')

from celery import Celery
from celery.schedules import crontab

from BookAppAPI.settings.celery import CELERY

app = Celery('proj')
app.config_from_object(CELERY)
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'get_user_recommendations': {
        'task': 'recommendations.tasks.get_user_recommendations',
        'schedule': crontab(hour=23, minute=0)
    },
}
