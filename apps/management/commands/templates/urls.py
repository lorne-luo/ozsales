URLS_HEADER = '''from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views


urlpatterns = []
router = DefaultRouter()
router.include_root_view = False
'''

URLS_MODEL_TEMPLATE = '''
# urls for <% model_name %>
urlpatterns += patterns('',
    url(r'^<% app_name %>/<% model_name %>/add/$', login_required(views.<% MODEL_NAME %>AddView.as_view()), name="<% model_name %>-add"),
    url(r'^<% app_name %>/<% model_name %>/list/$', login_required(views.<% MODEL_NAME %>ListView.as_view()), name='<% model_name %>-list'),
    url(r'^<% app_name %>/<% model_name %>/(?P<pk>\d+)/$', login_required(views.<% MODEL_NAME %>DetailView.as_view()), name="<% model_name %>-detail"),
    url(r'^<% app_name %>/<% model_name %>/(?P<pk>\d+)/edit/$', login_required(views.<% MODEL_NAME %>UpdateView.as_view()), name="<% model_name %>-update"),
    url(r'^<% app_name %>/<% model_name %>/delete/$', views.<% MODEL_NAME %>DeleteView.as_view(), name='<% model_name %>-delete'),
)

# reverse('api-<% model_name %>-list'),reverse('api-<% model_name %>-detail', kwargs={'pk': 1})
router.register(r'api/<% app_name %>/<% model_name %>', views.<% MODEL_NAME %>ViewSet, base_name='api-<% model_name %>')

'''

URLS_FOOTER = '''
urlpatterns += router.urls
'''