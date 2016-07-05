from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views

urlpatterns = []
router = DefaultRouter()
router.include_root_view = False

urlpatterns = patterns('',
    url(r'^product/$', views.ProductListView.as_view(), name="product-list"),
    url(r'^product/add/$', views.ProductAddEdit.as_view(), name="product-add"),
    url(r'^product/edit/(?P<pk>\d+)/$', views.ProductAddEdit.as_view(), name="product-edit"),
    url(r'^product/product/list/$', views.ProductListView.as_view(), name='product-list-view'),
    url(r'^product/product/add/$', login_required(views.ProductAddView.as_view()), name="product-add-view"),
    url(r'^product/product/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name="product-detail"),
    url(r'^product/product/(?P<pk>\d+)/edit/$', login_required(views.ProductUpdateView.as_view()), name="product-update"),
    # url(r'^product/delete/$', login_required(views.ProductListView.as_view()), name="product-delete-view"),
)

# reverse('product:api-product-list'), reverse('product:api-product-detail', kwargs={'pk': 1})
router.register(r'api/product/product', views.ProductViewSet, base_name='api-product')


# urls for brand
urlpatterns += patterns('',
    url(r'^product/brand/add/$', login_required(views.BrandAddView.as_view()), name='brand-add'),
    url(r'^product/brand/list/$', login_required(views.BrandListView.as_view()), name='brand-list'),
    url(r'^product/brand/(?P<pk>\d+)/$', login_required(views.BrandDetailView.as_view()), name='brand-detail'),
    url(r'^product/brand/(?P<pk>\d+)/edit/$', login_required(views.BrandUpdateView.as_view()), name='brand-update'),
)

# reverse('product:api-brand-list'), reverse('product:api-brand-detail', kwargs={'pk': 1})
router.register(r'api/product/brand', views.BrandViewSet, base_name='api-brand')


urlpatterns += router.urls