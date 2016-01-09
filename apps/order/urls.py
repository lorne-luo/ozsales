__author__ = 'Lorne'

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('apps.order.views',
    url(r'^order/(?P<order_id>\d+)/(?P<status_str>\w+)/$', views.change_order_status, name='change-order-status'),
    url(r'^order/paid/(?P<order_id>\d+)/$', views.change_order_paid, name="change-order-paid"),

    url(r'^$', views.OrderIndex.as_view(), name="order-index"),
	url(r'^add/$', views.OrderAddEdit.as_view(), name="order-add"),
	url(r'^edit/(?P<pk>\d+)/$', views.OrderAddEdit.as_view(), name="order-edit"),
    url(r'^/(?P<order_id>\d+)/(?P<status_str>\w+)/$', views.change_order_status, name="change-order-status"),
)