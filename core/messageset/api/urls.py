from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:notification-list'),reverse('api:notification-detail', kwargs={'pk': 1})
router.register(r'notification', views.NotificationViewSet, base_name='notification')
# router.register(r'notificationcontent', views.NotificationContentViewSet, base_name='notificationcontent')
router.register(r'sitemailcontent', views.SiteMailContentViewSet, base_name='sitemailcontent')
router.register(r'sitemailreceive', views.SiteMailReceiveViewSet, base_name='sitemailreceive')
router.register(r'sitemailsend', views.SiteMailSendViewSet, base_name='sitemailsend')
router.register(r'task', views.TaskViewSet, base_name='task')

urlpatterns = [
    url(r'sitemail/receive/markall', views.sitemail_markall, name='sitemail_markall'),
    url(r'notification/markall', views.notification_markall, name='notification_markall'),
]

urlpatterns += router.urls
