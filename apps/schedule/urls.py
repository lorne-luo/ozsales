# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views


urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False

# urls for dealtask
urlpatterns += patterns('',
    url(r'^schedule/dealtask/add/$', login_required(views.DealTaskAddView.as_view()), name='dealtask-add'),
    url(r'^schedule/dealtask/list/$', login_required(views.DealTaskListView.as_view()), name='dealtask-list'),
    url(r'^schedule/dealtask/(?P<pk>\d+)/$', login_required(views.DealTaskDetailView.as_view()), name='dealtask-detail'),
    url(r'^schedule/dealtask/(?P<pk>\d+)/edit/$', login_required(views.DealTaskUpdateView.as_view()), name='dealtask-update'),
)


# reverse('schedule:api-dealtask-list'), reverse('schedule:api-dealtask-detail', kwargs={'pk': 1})
router.register(r'api/schedule/dealtask', views.DealTaskViewSet, base_name='api-dealtask')


urlpatterns += router.urls
