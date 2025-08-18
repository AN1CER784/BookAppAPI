import sys

from django.conf import settings


TESTING = 'test' in sys.argv
TESTING = TESTING or 'test_coverage' in sys.argv or 'pytest' in sys.modules

CELERY = {
    'broker_url': 'redis://localhost:6379/0',
    'task_always_eager': TESTING,
    'timezone': settings.TIME_ZONE,
    'result_backend': 'django-db',
    'result_extended': True,
    'task_track_started': True,
}
