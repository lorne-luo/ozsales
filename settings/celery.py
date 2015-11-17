from __future__ import absolute_import
import datetime
import os
import urllib
from celery import Celery
from django.conf import settings
from celery.task import periodic_task
from celery.task.schedules import crontab
from decimal import Decimal
from settings.settings import rate

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
app = Celery('settings')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@periodic_task(run_every=crontab(minute=0, hour='0,3,6,9,12,15,18,21'))
def get_aud_rmb():
    url = 'http://download.finance.yahoo.com/d/quotes.csv?s=AUDCNY=X&f=sl1d1t1ba&e=.csv'
    content = urllib.urlopen(url).read()
    try:
        if content.startswith('"AUDCNY'):
            infos = content.split(',')
            r = Decimal(infos[1])
            rate.aud_rmb_rate = r
            return r
            #rate.save()
    except:
        #print(0)
        return 0