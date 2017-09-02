# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views


urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False

# urls for DealSubscribe
urlpatterns += patterns('',
                        url(r'^schedule/dealsubscribe/add/$', login_required(views.DealSubscribeAddView.as_view()), name='dealsubscribe-add'),
                        url(r'^schedule/dealsubscribe/list/$', login_required(views.DealSubscribeListView.as_view()), name='dealsubscribe-list'),
                        url(r'^schedule/dealsubscribe/(?P<pk>\d+)/$', login_required(views.DealSubscribeDetailView.as_view()), name='dealsubscribe-detail'),
                        url(r'^schedule/dealsubscribe/(?P<pk>\d+)/edit/$', login_required(views.DealSubscribeUpdateView.as_view()), name='dealsubscribe-update'),
                        )


# reverse('schedule:api-dealsubscribe-list'), reverse('schedule:api-dealsubscribe-detail', kwargs={'pk': 1})
router.register(r'api/schedule/dealsubscribe', views.DealSubscribeViewSet, base_name='api-dealsubscribe')


urlpatterns += router.urls
