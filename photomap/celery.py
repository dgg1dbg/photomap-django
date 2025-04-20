from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photomap.settings')
app = Celery('photomap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()