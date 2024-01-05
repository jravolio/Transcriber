import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transcriber_project.settings")
app = Celery("transcriber_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()