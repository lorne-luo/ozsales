# -*- coding: utf-8 -*-
import logging
from celery.task import periodic_task, task
from celery.schedules import crontab
from apps.order.models import Order, ORDER_STATUS
from apps.tenant.models import Tenant

log = logging.getLogger(__name__)


# @periodic_task(run_every=crontab(minute=7, hour='9,12,15,18,21,0'))
@task
def update_delivery_tracking():
    for order in Order.objects.filter(status=ORDER_STATUS.SHIPPING):
        if not order.seller.is_premium:
            continue
        order.update_track()


# @periodic_task(run_every=crontab(minute=5, hour='11,14,17,19,23'))
@task
def send_delivery_sms():
    for tenant in Tenant.objects.normal():
        tenant.set_schema()
        for order in Order.objects.filter(status=ORDER_STATUS.DELIVERED):
            if not order.seller.is_premium:
                continue
            if not order.delivery_msg_sent:
                order.sms_delivered()
            order.set_status(ORDER_STATUS.FINISHED)

        for order in Order.objects.filter(status=ORDER_STATUS.SHIPPING):
            if not order.seller.is_premium:
                continue
            order.sms_delivered()
            if order.is_all_delivered:
                order.set_status(ORDER_STATUS.FINISHED)
                order.express_orders.update(delivery_sms_sent=True)
