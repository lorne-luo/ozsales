
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views

urlpatterns = patterns('apps.order.views',
    url(r'^order/(?P<order_id>\d+)/status/(?P<status_str>\w+)/$', views.change_order_status, name='change-order-status'),
    url(r'^order/paid/(?P<order_id>\d+)/$', views.change_order_paid, name="change-order-paid"),

    url(r'^$', views.OrderIndex.as_view(), name="order-index"),
	url(r'^add/$', views.OrderAddEdit.as_view(), name="order-add"),
	url(r'^edit/(?P<pk>\d+)/$', views.OrderAddEdit.as_view(), name="order-edit"),
)

router = DefaultRouter()
router.include_root_view = False

# urls for order
urlpatterns += patterns('',
    url(r'^order/order/add/$', login_required(views.OrderAddView.as_view()), name="order-add"),
    url(r'^order/order/list/$', login_required(views.OrderListView.as_view()), name='order-list'),
    url(r'^order/order/(?P<pk>\d+)/$', login_required(views.OrderDetailView.as_view()), name="order-detail"),
    url(r'^order/order/(?P<pk>\d+)/edit/$', login_required(views.OrderUpdateView.as_view()), name="order-update"),
)

# reverse('api-order-list'),reverse('api-order-detail', kwargs={'pk': 1})
router.register(r'api/order/order', views.OrderViewSet, base_name='api-order')


# urls for orderproduct
urlpatterns += patterns('',
    url(r'^order/orderproduct/add/$', login_required(views.OrderProductAddView.as_view()), name="orderproduct-add"),
    url(r'^order/orderproduct/list/$', login_required(views.OrderProductListView.as_view()), name='orderproduct-list'),
    url(r'^order/orderproduct/(?P<pk>\d+)/$', login_required(views.OrderProductDetailView.as_view()), name="orderproduct-detail"),
    url(r'^order/orderproduct/(?P<pk>\d+)/edit/$', login_required(views.OrderProductUpdateView.as_view()), name="orderproduct-update"),
)

# reverse('api-orderproduct-list'),reverse('api-orderproduct-detail', kwargs={'pk': 1})
router.register(r'api/order/orderproduct', views.OrderProductViewSet, base_name='api-orderproduct')


urlpatterns += router.urls
