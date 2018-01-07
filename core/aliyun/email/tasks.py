# -*- coding: utf-8 -*-
import logging
import redis
from celery.task import task
from .smtp import send_email
from ...sms.telstra_api import MessageSender

log = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
ALIYUN_EMAIL_DAILY_COUNTER = 'ALIYUN_EMAIL_DAILY_COUNTER'


@task
def email_send_task(receivers, subject, html_content, text_content=None):
    counter = r.get(ALIYUN_EMAIL_DAILY_COUNTER) or 0
    counter = int(counter)
    if counter < 200:
        send_email(receivers, subject, html_content, text_content=None)
        r.set(ALIYUN_EMAIL_DAILY_COUNTER, counter + 1)
    else:
        # todo send from local
        msg = 'Aliyun email exceed daily free limitation.'
        log.warning('[EMAIL SENDER] %s' % msg)
