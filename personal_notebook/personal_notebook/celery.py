import os
from celery import Celery

# Django жобасының settings модулін көрсету
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_notebook.settings')

app = Celery('personal_notebook')

# Django settings-тегі CELERY-мен басталатын барлық конфигурацияны оқиды
app.config_from_object('django.conf:settings', namespace='CELERY')

# tasks.py ішіндегі барлық task-тарды автоматты түрде тіркейді
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
