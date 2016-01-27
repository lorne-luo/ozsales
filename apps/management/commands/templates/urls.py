URLS_HEADER = '''
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
import views
import serializers # do not remove this unused module


urlpatterns = []
'''

URLS_MODEL_TEMPLATE = '''
# urls for <% model_name %>

urlpatterns += patterns('',
    url(r'^<% model_name %>/add/$', login_required(views.<% MODEL_NAME %>AddView.as_view()), name="<% model_name %>-add"),
    url(r'^<% model_name %>/list/$', views.<% MODEL_NAME %>ListView.as_view(), name='<% model_name %>-list'),
    url(r'^<% model_name %>/(?P<pk>\d+)/$', login_required(views.<% MODEL_NAME %>DetailView.as_view()), name="<% model_name %>-detail"),
    url(r'^<% model_name %>/(?P<pk>\d+)/edit/$', login_required(views.<% MODEL_NAME %>UpdateView.as_view()), name="<% model_name %>-update"),
)
'''