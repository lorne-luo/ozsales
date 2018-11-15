# -*- coding: utf-8 -*-
import logging
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from celery.task import periodic_task, task
from celery.schedules import crontab

from apps.tenant.models import Tenant
from core.sms.telstra_api_v2 import send_au_sms
from .models import Sms
from core.aliyun.sms.service import send_cn_sms

log = logging.getLogger(__name__)


# @periodic_task(run_every=crontab(hour=3, minute=7, day_of_month=2))
@task
def cleanup_sms_history():
    three_month_ago = timezone.now() - relativedelta(months=7)
    for tenant in Tenant.objects.normal():
        tenant.set_schema()
        Sms.objects.filter(time__lt=three_month_ago).delete()
        log.info('[SMS] Cleanup sms history older than 3 months.')


@task
def task_send_cn_sms(business_id, phone_numbers, template_code, template_param=None):
    send_cn_sms(business_id, phone_numbers, template_code, template_param)


@task
def task_send_au_sms(to, body, app_name):
    send_au_sms(to, body, app_name)


def send_cn_sms_task(business_id, phone_numbers, template_code, template_param=None):
    task_send_cn_sms.apply_async(args=[business_id, phone_numbers, template_code, template_param])


def send_au_sms_task(to, body, app_name=None):
    task_send_au_sms.apply_async(args=[to, body, app_name])
