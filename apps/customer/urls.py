from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
import serializers

import views

urlpatterns = patterns('apps.customer.views',
    url(r'^$', views.CustomerList.as_view(), name="customer-list"),
    url(r'^add/$', views.CustomerAddEdit.as_view(), name="customer-add"),
    url(r'^edit/(?P<pk>\d+)/$', views.CustomerAddEdit.as_view(), name="customer-edit"),

    url(r'^customer/list$', login_required(views.CustomerListView.as_view()), name="customer-list-view"),
    url(r'^customer/add$', login_required(views.CustomerCreateView.as_view()), name="customer-add-view"),
    url(r'^customer/(?P<pk>\d+)/$', login_required(views.CustomerDetailView.as_view()), name="customer-detail-view"),
    url(r'^customer/(?P<pk>\d+)/edit/$', login_required(views.CustomerUpdateView.as_view()), name="customer-update-view"),
    url(r'^customer/(?P<pk>\d+)/delete/$', login_required(views.CustomerDeleteView.as_view()), name="customer-delete-view"),
)