import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Load config from Django settings, namespace='CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

# Celery Beat schedule
app.conf.beat_schedule = {
    'flag-suspicious-ips-every-hour': {
        'task': 'ip_tracking.tasks.flag_suspicious_ips',
        'schedule': crontab(minute=0),  # runs every hour at 0 minutes
    },
}

