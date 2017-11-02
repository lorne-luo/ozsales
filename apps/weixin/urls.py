# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views


urlpatterns = []

# urls for page
urlpatterns += patterns('',
    url(r'^wx/(?P<app_name>\w+)/login$', views.wx_login, name='login'),
    url(r'^wx/(?P<app_name>\w+)/auth$', views.wx_auth, name='auth'),
    url(r'^wx/(?P<app_name>\w+)/index', views.wx_index, name='index'),
    url(r'^wx/(?P<app_name>\w+)/pay_notify', views.wx_pay_notify, name='pay_notify'),
)
