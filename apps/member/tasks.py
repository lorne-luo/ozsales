import logging

from celery.schedules import crontab
from celery.task import periodic_task
from django.core.management import call_command

log = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour=2))
def clearsessions():
    call_command('clearsessions')
    log.info('[Session] Session clear.')
