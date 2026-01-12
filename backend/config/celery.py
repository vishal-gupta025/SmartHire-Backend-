import os
from celery import Celery

# 👇 THIS LINE IS CRITICAL
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("smarthire")

# 👇 THIS LOADS DJANGO SETTINGS
app.config_from_object("django.conf:settings", namespace="CELERY")

# 👇 THIS DISCOVERS tasks.py FILES
app.autodiscover_tasks()
