# -*- coding: utf-8 -*-
import logging

from celery.task import periodic_task
from celery.task.schedules import crontab

from apps.order.models import Order, ORDER_STATUS

log = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute='*/240', hour='7-0'))
def update_delivery_tracking():
    unfinished_order = Order.objects.filter(status=ORDER_STATUS.SHIPPING)
    for order in unfinished_order:
        order.update_track()
