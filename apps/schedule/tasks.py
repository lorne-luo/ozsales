from celery import Celery
from django.conf import settings
from celery.task import periodic_task
from celery.task.schedules import crontab

