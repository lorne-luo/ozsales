# -*- coding: utf-8 -*-
import logging
from dateutil.relativedelta import relativedelta
from celery.task import periodic_task
from celery.task.schedules import crontab
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from apps.order.models import Order, ORDER_STATUS
from .models import ExpressOrder

log = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute='*/240', hour='7-0'))
def update_delivery_tracking():
    now = timezone.now()
    three_days_ago = now - relativedelta(days=3)
    express_orders = ExpressOrder.objects.filter(order__status=ORDER_STATUS.SHIPPING, create_time__lt=three_days_ago)
    for order in express_orders:
        order.update_track()

    week_ago = now - relativedelta(days=5)
    unfinished_order = Order.objects.filter(status=ORDER_STATUS.SHIPPING, ship_time__lt=week_ago)
    for order in unfinished_order:
        if order.seller.check_premium_member():
            delivered = [express.is_delivered for express in order.express_orders.all()]
            if all(delivered):
                order.set_status(ORDER_STATUS.DELIVERED)
                # notify seller
                subject = u'%s is already delivered.' % order
                link = reverse('order-detail-short', args=[order.customer.id, order.id])
                content = u'%s is already delivered. <a href="%s%s">click here</a> to check.' % (order, settings.DOMAIN_URL, link)
                order.seller.send_email(subject, content)
                order.customer.send_email(subject, content)
