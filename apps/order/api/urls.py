from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views

urlpatterns = [
   # url(r'^now/$', views.ChannelViewSet.as_view({'get': 'now_and_next_event'}),
   #     name="channel-event-now-and-next"),
]
router = PostHackedRouter()
router.include_root_view = False
router.register(r'order', views.OrderViewSet, 'order')

urlpatterns += router.urls
