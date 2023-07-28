import os
import time

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NKO.settings')

app = Celery('nko')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://redis:6379/0'
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    time.sleep(20)
    print('Hello form debug_task')
