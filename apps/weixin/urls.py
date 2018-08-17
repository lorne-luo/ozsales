# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
from . import views


urlpatterns = []

# urls for page
urlpatterns += (
    url(r'^(?P<app_name>\w+)/login$', views.wx_login, name='login'),
    url(r'^(?P<app_name>\w+)/auth$', views.wx_auth, name='auth'),
    url(r'^(?P<app_name>\w+)/index', views.wx_index, name='index'),
    url(r'^(?P<app_name>\w+)/pay_notify', views.wx_pay_notify, name='pay_notify'),
)
