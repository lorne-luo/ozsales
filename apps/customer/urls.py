from django.conf.urls import patterns, url

import views

urlpatterns = patterns('apps.customer.views',
    url(r'^$', views.CustomerList.as_view(), name="customer-list"),
	url(r'^add/$', views.CustomerAddEdit.as_view(), name="customer-add"),
	url(r'^edit/(?P<pk>\d+)/$', views.CustomerAddEdit.as_view(), name="customer-edit"),
)