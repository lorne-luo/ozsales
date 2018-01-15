# -*- coding: utf-8 -*-
import logging
from celery.task import periodic_task
from celery.task.schedules import crontab
from apps.order.models import Order, ORDER_STATUS

log = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute='*/240', hour='7-0'))
def update_delivery_tracking():
    for order in Order.objects.filter(status__in=[ORDER_STATUS.SHIPPING, ORDER_STATUS.CREATED]):
        if not order.seller.check_premium_member():
            continue
        order.update_track()
