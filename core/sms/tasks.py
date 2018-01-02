# -*- coding: utf-8 -*-
import logging
import redis
from celery.task import periodic_task
from celery.task.schedules import crontab

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
TELSTRA_SMS_MONTHLY_COUNTER = 'TELSTRA_SMS_MONTHLY_COUNTER'


@periodic_task(run_every=crontab(hour=0, minute=1, day_of_month=1))
def reset_sms_monthly_counter():
    r.set(TELSTRA_SMS_MONTHLY_COUNTER, 0)
