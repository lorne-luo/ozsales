API_URLS_HEADER = '''# coding=utf-8
from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views


urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False
'''

API_URLS_BODY = '''
# reverse('api:<% model_name %>-list'), reverse('api:<% model_name %>-detail', kwargs={'pk': 1})
router.register(r'api/<% app_name %>/<% model_name %>', views.<% MODEL_NAME %>ViewSet, base_name='api-<% model_name %>')

'''

API_URLS_FOOTER = '''
urlpatterns += router.urls
'''
