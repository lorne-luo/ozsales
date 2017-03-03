# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views
import views_api

urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False

# urlpatterns = patterns('apps.customer.views',
#     url(r'^$', views.CustomerList.as_view(), name="customer-list"),
#     url(r'^add/$', views.CustomerAddEdit.as_view(), name="customer-add"),
#     url(r'^edit/(?P<pk>\d+)/$', views.CustomerAddEdit.as_view(), name="customer-edit"),
#
#     url(r'^customer/list/$', login_required(views.CustomerListView.as_view()), name="customer-list-view"),
#     url(r'^customer/add/$', login_required(views.CustomerCreateView.as_view()), name="customer-add-view"),
#     url(r'^customer/(?P<pk>\d+)/$', login_required(views.CustomerDetailView.as_view()), name="customer-detail-view"),
#     url(r'^customer/(?P<pk>\d+)/edit/$', login_required(views.CustomerUpdateView.as_view()), name="customer-update-view"),
#     url(r'^customer/delete/$', login_required(views.CustomerDeleteView.as_view()), name="customer-delete-view"),
# )

# urls for address
urlpatterns += patterns('',
    url(r'^customer/address/add/$', login_required(views.AddressAddView.as_view()), name='address-add'),
    url(r'^customer/address/list/$', login_required(views.AddressListView.as_view()), name='address-list'),
    url(r'^customer/address/(?P<pk>\d+)/$', login_required(views.AddressDetailView.as_view()), name='address-detail'),
    url(r'^customer/address/(?P<pk>\d+)/edit/$', login_required(views.AddressUpdateView.as_view()), name='address-update'),
)

# reverse('customer:api-address-list'), reverse('customer:api-address-detail', kwargs={'pk': 1})
router.register(r'api/customer/address', views.AddressViewSet, base_name='api-address')


# urls for customer
urlpatterns += patterns('',
    url(r'^customer/customer/add/$', login_required(views.CustomerAddView.as_view()), name='customer-add'),
    url(r'^customer/customer/list/$', login_required(views.CustomerListView.as_view()), name='customer-list'),
    url(r'^customer/customer/(?P<pk>\d+)/$', login_required(views.CustomerDetailView.as_view()), name='customer-detail'),
    url(r'^customer/customer/(?P<pk>\d+)/edit/$', login_required(views.CustomerUpdateView.as_view()), name='customer-update'),
)

urlpatterns += patterns('',
    url(r'^customer/add_cart', login_required(views_api.AddCart.as_view()), base_name='api-add-cart'),
)

# reverse('customer:api-customer-list'), reverse('customer:api-customer-detail', kwargs={'pk': 1})
router.register(r'api/customer/customer', views.CustomerViewSet, base_name='api-customer')

urlpatterns += router.urls