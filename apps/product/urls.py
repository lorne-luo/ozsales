from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^product/add/$', views.ProductAddView.as_view(), name="product-add"),
    url(r'^product/$', views.ProductListView.as_view(), name="product-list"),
    url(r'^product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name="product-detail"),
    url(r'^product/(?P<pk>\d+)/edit/$', views.ProductUpdateView.as_view(), name="product-update"),
]

# urls for brand
urlpatterns += [
    url(r'^brand/add/$', views.BrandAddView.as_view(), name='brand-add'),
    url(r'^brand/list/$', views.BrandListView.as_view(), name='brand-list'),
    url(r'^brand/(?P<pk>\d+)/$', views.BrandDetailView.as_view(), name='brand-detail'),
    url(r'^brand/(?P<pk>\d+)/edit/$', views.BrandUpdateView.as_view(), name='brand-update'),
]
