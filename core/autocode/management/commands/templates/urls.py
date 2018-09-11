URLS_HEADER = '''# coding=utf-8
from django.conf.urls import url
from . import views


urlpatterns = []
'''

URLS_BODY = '''
# urls for <% model_name %>
urlpatterns += patterns('',
    url(r'^<% app_name %>/<% model_name %>/add/$', views.<% MODEL_NAME %>AddView.as_view(), name='<% model_name %>-add'),
    url(r'^<% app_name %>/<% model_name %>/list/$', views.<% MODEL_NAME %>ListView.as_view(), name='<% model_name %>-list'),
    url(r'^<% app_name %>/<% model_name %>/(?P<pk>[-\w]+)/$', views.<% MODEL_NAME %>DetailView.as_view(), name='<% model_name %>-detail'),
    url(r'^<% app_name %>/<% model_name %>/(?P<pk>[-\w]+)/edit/$', views.<% MODEL_NAME %>UpdateView.as_view(), name='<% model_name %>-update'),
)

'''

URLS_FOOTER = ''
