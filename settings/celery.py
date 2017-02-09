from __future__ import absolute_import

import os
from decimal import Decimal
from celery import Celery
from celery.task import periodic_task
from celery.task.schedules import crontab
from django.conf import settings
from yahoo_finance import Currency

from core.sms.telstra_api import MessageSender
from settings.settings import rate

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
app = Celery('settings')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@periodic_task(run_every=crontab(minute=0, hour='8,12,16,20',day_of_week='mon,tue,wed,thu,fri'))
def get_aud_rmb():
    # url = 'http://download.finance.yahoo.com/d/quotes.csv?s=AUDCNY=X&f=sl1d1t1ba&e=.csv'
    audcny = Currency('AUDCNY')
    value = audcny.get_rate()
    rate.aud_rmb_rate = Decimal(value)
    sender = MessageSender()
    sender.send_to_self(value)

    return rate.aud_rmb_rate
