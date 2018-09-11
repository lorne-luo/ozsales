# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

# urls for DealSubscribe
urlpatterns = (
    url(r'^dealsubscribe/add/$', login_required(views.DealSubscribeAddView.as_view()), name='dealsubscribe-add'),
    url(r'^dealsubscribe/list/$', login_required(views.DealSubscribeListView.as_view()), name='dealsubscribe-list'),
    url(r'^dealsubscribe/(?P<pk>[-\w]+)/$', login_required(views.DealSubscribeDetailView.as_view()), name='dealsubscribe-detail'),
    url(r'^dealsubscribe/(?P<pk>[-\w]+)/edit/$', login_required(views.DealSubscribeUpdateView.as_view()), name='dealsubscribe-update'),
)

