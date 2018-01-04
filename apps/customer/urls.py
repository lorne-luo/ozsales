# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views
import views_api

urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False

# urls for address
urlpatterns += [
    url(r'^customer/address/add/$', login_required(views.AddressAddView.as_view()), name='address-add'),
    url(r'^customer/address/list/$', login_required(views.AddressListView.as_view()), name='address-list'),
    url(r'^customer/address/(?P<pk>\d+)/$', login_required(views.AddressDetailView.as_view()), name='address-detail'),
    url(r'^customer/address/(?P<pk>\d+)/edit/$', login_required(views.AddressUpdateView.as_view()), name='address-update'),
    url(r'^customer/address/autocomplete/$', views_api.AddressAutocomplete.as_view(), name='address-autocomplete'),
]

# reverse('customer:api-address-list'), reverse('customer:api-address-detail', kwargs={'pk': 1})
router.register(r'api/customer/address', views.AddressViewSet, base_name='api-address')


# urls for customer
urlpatterns += [
    url(r'^customer/customer/add/$', login_required(views.CustomerAddView.as_view()), name='customer-add'),
    url(r'^customer/customer/list/$', login_required(views.CustomerListView.as_view()), name='customer-list'),
    url(r'^customer/customer/(?P<pk>\d+)/$', login_required(views.CustomerDetailView.as_view()), name='customer-detail'),
    url(r'^customer/customer/(?P<pk>\d+)/edit/$', login_required(views.CustomerUpdateView.as_view()), name='customer-update'),
    url(r'^customer/customer/autocomplete/$', views_api.CustomerAutocomplete.as_view(), name='customer-autocomplete'),
]

urlpatterns += [
    url(r'^customer/add_cart', views_api.AddCart.as_view(), name='api-add-cart'),
]

# reverse('customer:api-customer-list'), reverse('customer:api-customer-detail', kwargs={'pk': 1})
router.register(r'api/customer/customer', views.CustomerViewSet, base_name='api-customer')

urlpatterns += router.urls