"""Module for celery instance for 'nimble' project."""
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    "config",
    broker="redis://127.0.0.1:6379",
    backend="redis://127.0.0.1:6379",
    include=["api.tasks"],
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_contacts_table_with_api_data": {
        "task": "api.tasks.run_updating_contacts",
        "schedule": crontab(hour="4", minute="5"),
    }
}
