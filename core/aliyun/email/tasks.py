# -*- coding: utf-8 -*-
import logging
import redis
from celery.task import task, periodic_task
from celery.task.schedules import crontab
from .smtp import send_email
from ...sms.telstra_api import MessageSender

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
ALIYUN_DAILY_EMAIL_COUNTER = 'ALIYUN_DAILY_EMAIL_COUNTER'


@task
def email_send_task(receivers, subject, html_content, text_content=None):
    counter = r.get(ALIYUN_DAILY_EMAIL_COUNTER) or 0
    if counter < 200:
        send_email(receivers, subject, html_content, text_content=None)
        r.set(ALIYUN_DAILY_EMAIL_COUNTER, counter + 1)
    else:
        # todo send from local
        msg = 'Aliyun email exceed daily free limitation.'
        MessageSender().send_to_self(msg, 'EMAIL_SENDER')
        log.info('[EMAIL SENDER] %s' % msg)


@periodic_task(run_every=crontab(hour=0, minute=1))
def reset_email_daily_counter():
    r.set(ALIYUN_DAILY_EMAIL_COUNTER, 0)
