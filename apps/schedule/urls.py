# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

# urls for DealSubscribe
urlpatterns = (
    url(r'^schedule/dealsubscribe/add/$', login_required(views.DealSubscribeAddView.as_view()), name='dealsubscribe-add'),
    url(r'^schedule/dealsubscribe/list/$', login_required(views.DealSubscribeListView.as_view()), name='dealsubscribe-list'),
    url(r'^schedule/dealsubscribe/(?P<pk>\d+)/$', login_required(views.DealSubscribeDetailView.as_view()), name='dealsubscribe-detail'),
    url(r'^schedule/dealsubscribe/(?P<pk>\d+)/edit/$', login_required(views.DealSubscribeUpdateView.as_view()), name='dealsubscribe-update'),
)

