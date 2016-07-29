# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views


urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False

# urls for expresscarrier
urlpatterns += patterns('',
    url(r'^express/expresscarrier/add/$', login_required(views.ExpressCarrierAddView.as_view()), name='expresscarrier-add'),
    url(r'^express/expresscarrier/list/$', login_required(views.ExpressCarrierListView.as_view()), name='expresscarrier-list'),
    url(r'^express/expresscarrier/(?P<pk>\d+)/$', login_required(views.ExpressCarrierDetailView.as_view()), name='expresscarrier-detail'),
    url(r'^express/expresscarrier/(?P<pk>\d+)/edit/$', login_required(views.ExpressCarrierUpdateView.as_view()), name='expresscarrier-update'),
)


# reverse('express:api-expresscarrier-list'), reverse('express:api-expresscarrier-detail', kwargs={'pk': 1})
router.register(r'api/express/expresscarrier', views.ExpressCarrierViewSet, base_name='api-expresscarrier')


# # urls for expressorder
# urlpatterns += patterns('',
#     url(r'^express/expressorder/add/$', login_required(views.ExpressOrderAddView.as_view()), name='expressorder-add'),
#     url(r'^express/expressorder/list/$', login_required(views.ExpressOrderListView.as_view()), name='expressorder-list'),
#     url(r'^express/expressorder/(?P<pk>\d+)/$', login_required(views.ExpressOrderDetailView.as_view()), name='expressorder-detail'),
#     url(r'^express/expressorder/(?P<pk>\d+)/edit/$', login_required(views.ExpressOrderUpdateView.as_view()), name='expressorder-update'),
# )
#
#
# # reverse('express:api-expressorder-list'), reverse('express:api-expressorder-detail', kwargs={'pk': 1})
# router.register(r'api/express/expressorder', views.ExpressOrderViewSet, base_name='api-expressorder')


urlpatterns += router.urls
