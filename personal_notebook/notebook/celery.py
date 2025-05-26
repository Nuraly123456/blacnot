from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_notebook.settings')
app = Celery('personal_notebook')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-news-every-day': {
        'task': 'notebook.tasks.update_news_daily',
        'schedule': 86400,  # 24 сағат сайын
    },
}