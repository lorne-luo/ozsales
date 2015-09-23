from __future__ import absolute_import
import datetime
import os
from celery import Celery
from django.conf import settings
from celery.task import periodic_task
from celery.task.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
app = Celery('settings')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@periodic_task(run_every=crontab(minute="*/1"))
def get_aud_rmb_rate():
    print('Request: {0!r')



#import dbsettings
#class EmailOptions(dbsettings.Group):
#    enabled = dbsettings.BooleanValue('whether to send emails or not')
#	    sender = dbsettings.StringbbValue('address to send emails from')
#		    subject = dbsettings.StringValue(default='SiteMail')
#
#			email = EmailOptions()
