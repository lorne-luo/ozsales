# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import views

# urls for page
urlpatterns = (
    url(r'^page/add/$', login_required(views.PageAddView.as_view()), name='page-add'),
    url(r'^page/list/$', login_required(views.PageListView.as_view()), name='page-list'),
    url(r'^page/(?P<pk>\d+)/$', login_required(views.PageDetailView.as_view()), name='page-detail'),
    url(r'^page/(?P<pk>\d+)/edit/$', login_required(views.PageUpdateView.as_view()), name='page-update'),
)

# urls for store
urlpatterns += (
    url(r'^store/add/$', login_required(views.StoreAddView.as_view()), name='store-add'),
    url(r'^store/list/$', login_required(views.StoreListView.as_view()), name='store-list'),
    url(r'^store/(?P<pk>\d+)/$', login_required(views.StoreDetailView.as_view()), name='store-detail'),
    url(r'^store/(?P<pk>\d+)/edit/$', login_required(views.StoreUpdateView.as_view()), name='store-update'),
)
