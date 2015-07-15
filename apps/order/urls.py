__author__ = 'Lorne'

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('apps.order.views',
    url(r'^order/(?P<order_id>\d+)/(?P<status_str>\w+)/$', views.change_order_status, name="change-order-status"),
)