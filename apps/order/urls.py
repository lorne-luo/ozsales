
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()
router.include_root_view = False

urlpatterns = patterns('apps.order.views',
    url(r'^order/(?P<order_id>\d+)/status/(?P<status_value>\w+)/$', views.change_order_status, name='change-order-status'),
    url(r'^order/paid/(?P<order_id>\d+)/$', views.change_order_paid, name="change-order-paid"),

    url(r'^order/index/$', views.OrderIndex.as_view(), name="order-index"),
	# url(r'^add/$', views.OrderAddEdit.as_view(), name="order-add"),
	# url(r'^order/edit/(?P<pk>\d+)/$', views.OrderAddEdit.as_view(), name="order-edit"),
    url(r'^order/(?P<customer_id>\d+)/(?P<pk>\d+)/$', views.OrderDetailView.as_view(), name='order-detail'),
    url(r'^(?P<customer_id>\d+)/(?P<pk>\d+)/$', views.OrderDetailView.as_view(), name='order-detail-short'),
    url(r'^order/(?P<pk>\d+)/edit/$', login_required(views.OrderUpdateView.as_view()), name='order-update'),
    url(r'^order/add/$', login_required(views.OrderAddView.as_view()), name='order-add'),
    url(r'^order/add/(?P<customer_id>\d+)/$', login_required(views.OrderAddDetailView.as_view()), name='order-add-detail'),
    url(r'^order/list/$', login_required(views.OrderListView.as_view()), name='order-list'),
    url(r'^order/$', login_required(views.OrderListView.as_view()), name='order-list-short'),
    url(r'^order/(?P<username>\w+)/$', views.OrderMemberListView.as_view(), name='order-member'),
)


# reverse('order:api-order-list'), reverse('order:api-order-detail', kwargs={'pk': 1})
router.register(r'api/order/order', views.OrderViewSet, base_name='api-order')


urlpatterns += router.urls