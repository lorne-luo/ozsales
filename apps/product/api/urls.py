from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
import views

urlpatterns = patterns('',
                       # url(r'^now/$', views.ChannelViewSet.as_view({'get': 'now_and_next_event'}),
                       #     name="channel-event-now-and-next"),
                       )
router = DefaultRouter()
router.include_root_view = False
router.register(r'product', views.ProductViewSet, base_name='api-product')

urlpatterns += router.urls
