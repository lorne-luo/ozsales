from django.conf.urls import patterns, url

import views

urlpatterns = patterns('apps.product.views',
    url(r'^$', views.ProductList.as_view(), name="product-list"),
	url(r'^add/$', views.ProductAddEdit.as_view(), name="product-add"),
	url(r'^edit/(?P<pk>\d+)/$', views.ProductAddEdit.as_view(), name="product-edit"),
)