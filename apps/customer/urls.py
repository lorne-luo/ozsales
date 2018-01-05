# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^customer/address/add/$', views.AddressAddView.as_view(), name='address-add'),
    url(r'^customer/address/list/$', views.AddressListView.as_view(), name='address-list'),
    url(r'^customer/address/(?P<pk>\d+)/$', views.AddressDetailView.as_view(), name='address-detail'),
    url(r'^customer/address/(?P<pk>\d+)/edit/$', views.AddressUpdateView.as_view(), name='address-update'),
]

# urls for customer
urlpatterns += [
    url(r'^customer/customer/add/$', views.CustomerAddView.as_view(), name='customer-add'),
    url(r'^customer/customer/list/$', views.CustomerListView.as_view(), name='customer-list'),
    url(r'^customer/customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name='customer-detail'),
    url(r'^customer/customer/(?P<pk>\d+)/edit/$', views.CustomerUpdateView.as_view(), name='customer-update'),
]
