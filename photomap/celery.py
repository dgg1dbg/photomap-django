from celery import Celery

app = Celery('photomap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()