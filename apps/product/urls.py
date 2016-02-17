from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
import views
import serializers


urlpatterns = patterns('',
    url(r'^$', views.ProductList.as_view(), name="product-list"),
    url(r'^add/$', views.ProductAddEdit.as_view(), name="product-add"),
    url(r'^edit/(?P<pk>\d+)/$', views.ProductAddEdit.as_view(), name="product-edit"),
    url(r'^product/list/$', views.ProductListView.as_view(), name='product-list-view'),
    url(r'^product/add/$', login_required(views.ProductAddView.as_view()), name="product-add-view"),
    url(r'^product/(?P<pk>\d+)/$', login_required(views.ProductDetailView.as_view()), name="product-detail-view"),
    url(r'^product/(?P<pk>\d+)/edit/$', login_required(views.ProductUpdateView.as_view()), name="product-update-view"),
    # url(r'^product/delete/$', login_required(views.ProductListView.as_view()), name="product-delete-view"),

    # public product api
    url(r'api/product/list/$', views.PublicListAPIView.as_view(), name='allowany-product-list'),
)