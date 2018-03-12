# -*- coding: utf-8 -*-
import logging
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from celery.task import periodic_task
from celery.task.schedules import crontab
from .models import Sms

log = logging.getLogger(__name__)


@periodic_task(run_every=crontab(hour=1, minute=6, day_of_month=2))
def cleanup_sms_history():
    three_month_ago = timezone.now() - relativedelta(months=3)
    Sms.objects.filter(time__lt=three_month_ago).delete()
    log.info('[SMS] Cleanup sms history older than 3 months.')