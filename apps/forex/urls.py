# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

# urls for page
urlpatterns = (
    url(r'^btcusdt/$', views.ForexIndexView.as_view(), name='btcusdt'),
    url(r'^$', views.BTCUSDTView.as_view(), name='main'),
)
