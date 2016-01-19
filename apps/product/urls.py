from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.ProductList.as_view(), name="product-list"),
	url(r'^add/$', views.ProductAddEdit.as_view(), name="product-add"),
	url(r'^edit/(?P<pk>\d+)/$', views.ProductAddEdit.as_view(), name="product-edit"),
    url(r'^list/$', views.ProductListView.as_view(), name='new-product-list'),
)