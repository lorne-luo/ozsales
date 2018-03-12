from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^order/add/$', views.OrderAddView.as_view(), name='order-add'),
    url(r'^order/add/(?P<customer_id>\d+)/$', views.OrderAddDetailView.as_view(), name='order-add-detail'),
    url(r'^order/list/$', views.OrderListView.as_view(), name='order-list'),
    url(r'^order/(?P<pk>\d+)/edit/$', views.OrderUpdateView.as_view(), name='order-update'),
    url(r'^order/(?P<customer_id>\d+)/(?P<pk>\d+)/$', views.OrderDetailView.as_view(), name='order-detail'),

    url(r'^order/index/$', views.OrderIndex.as_view(), name="order-index"),
    url(r'^$', views.OrderListView.as_view(), name='order-list-short'),
    url(r'^(?P<customer_id>\d+)/(?P<pk>\d+)/$', views.OrderDetailView.as_view()),
    url(r'^order/(?P<username>\w+)/$', views.OrderMemberListView.as_view(), name='order-member'),
    url(r'^order/(?P<order_id>\d+)/status/(?P<status_value>\w+)/$', views.change_order_status, name='change-order-status'),
    url(r'^order/paid/(?P<order_id>\d+)/$', views.change_order_paid, name="change-order-paid"),

    # payment
    url(r'^order/(?P<pk>\d+)/pay/$', views.OrderPayView.as_view(), name='order-pay'),
]

# urls for orderproduct
urlpatterns += [
    url(r'^orderproduct/list/$', views.OrderProductListView.as_view(), name='orderproduct-list'),
    url(r'^orderproduct/(?P<pk>\d+)/$', views.OrderProductDetailView.as_view(), name='orderproduct-detail')
]
