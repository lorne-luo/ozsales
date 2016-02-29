from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
import views


# Page URL
urlpatterns = [

    # url(r'/page/(?P<app_name>\w+)/(?P<model_name>\w+)/form.html$',
    # TemplateView.as_view(template_name='adminlte/system/config.html'),
    # name='common_form'),
    #
    # url(r'/page/adminlte/SystemConfig.html$',
    #     TemplateView.as_view(template_name='adminlte/system/config.html'),
    #     name='systemconfig'),
    # url(r'/system/config/form.html$', SystemConfigFormView.as_view(),
    #     name='systemconfig_form'),
    #
    # url(r'/system/role.html$', SiteMailListView.as_view(),
    #     name='role'),
    # url(r'/system/auth.html$', SiteMailListView.as_view(),
    #     name='auth'),
    # url(r'/system/user.html$', SiteMailListView.as_view(),
    #     name='user'),
    #
    # url(r'/page/adminlte/SiteMail.html$', SiteMailListView.as_view(),
    #     name='sitemail'),
    # url(r'/notification.html$', NotificationListView.as_view(),
    #     name='notification'),
    # url(r'/task.html$', TaskListView.as_view(),
    #     name='task'),
]
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
import views


urlpatterns = []
router = DefaultRouter()
router.include_root_view = False

# urls for notification
urlpatterns += patterns('',
    url(r'^messageset/notification/list/$', login_required(views.NotificationListView.as_view()), name='notification-list'),
    url(r'^messageset/notification/(?P<pk>\d+)/$', login_required(views.NotificationDetailView.as_view()), name='notification-detail'),
    url(r'^messageset/notification/(?P<pk>\d+)/edit/$', login_required(views.NotificationUpdateView.as_view()), name='notification-update'),
)

# reverse('messageset:api-notification-list'),reverse('messageset:api-notification-detail', kwargs={'pk': 1})
router.register(r'api/messageset/notification', views.NotificationViewSet, base_name='api-notification')


# urls for notificationcontent
urlpatterns += patterns('',
    url(r'^messageset/notificationcontent/add/$', login_required(views.NotificationContentAddView.as_view()), name='notificationcontent-add'),
    url(r'^messageset/notificationcontent/(?P<pk>\d+)/$', login_required(views.NotificationContentDetailView.as_view()), name='notificationcontent-detail'),
    url(r'^messageset/notificationcontent/(?P<pk>\d+)/edit/$', login_required(views.NotificationContentUpdateView.as_view()), name='notificationcontent-update'),
)

# reverse('messageset:api-notificationcontent-list'),reverse('messageset:api-notificationcontent-detail', kwargs={'pk': 1})
router.register(r'api/messageset/notificationcontent', views.NotificationContentViewSet, base_name='api-notificationcontent')


# urls for sitemailcontent
urlpatterns += patterns('',
    url(r'^messageset/sitemail/add/$', login_required(views.SiteMailContentAddView.as_view()), name='sitemail-add'),
    url(r'^messageset/sitemailcontent/(?P<pk>\d+)/$', login_required(views.SiteMailContentDetailView.as_view()), name='sitemailcontent-detail'),
    url(r'^messageset/sitemailcontent/(?P<pk>\d+)/edit/$', login_required(views.SiteMailContentUpdateView.as_view()), name='sitemailcontent-update'),
)


# reverse('messageset:api-sitemailcontent-list'),reverse('messageset:api-sitemailcontent-detail', kwargs={'pk': 1})
router.register(r'api/messageset/sitemailcontent', views.SiteMailContentViewSet, base_name='api-sitemailcontent')


# urls for sitemailreceive
urlpatterns += patterns('',
    url(r'^messageset/sitemail/list/$', login_required(views.SiteMailReceiveListView.as_view()), name='sitemail-list'),
    url(r'^messageset/sitemail/receive/(?P<pk>\d+)/$', login_required(views.SiteMailReceiveDetailView.as_view()), name='sitemailreceive-detail'),
    url(r'api/messageset/sitemail/receive/markall', views.sitemail_markall, name='api-sitemail_markall'),
)

# reverse('messageset:api-sitemailreceive-list'),reverse('messageset:api-sitemailreceive-detail', kwargs={'pk': 1})
router.register(r'api/messageset/sitemailreceive', views.SiteMailReceiveViewSet, base_name='api-sitemailreceive')


# urls for sitemailsend
urlpatterns += patterns('',
    url(r'^messageset/sitemailsend/(?P<pk>\d+)/$', login_required(views.SiteMailSendDetailView.as_view()), name='sitemailsend-detail'),
)

# reverse('messageset:api-sitemailsend-list'),reverse('messageset:api-sitemailsend-detail', kwargs={'pk': 1})
router.register(r'api/messageset/sitemailsend', views.SiteMailSendViewSet, base_name='api-sitemailsend')


# urls for task
urlpatterns += patterns('',
    url(r'^messageset/task/list/$', login_required(views.TaskListView.as_view()), name='task-list'),
    url(r'^messageset/task/(?P<pk>\d+)/$', login_required(views.TaskDetailView.as_view()), name='task-detail'),
    # url(r'^messageset/task/(?P<pk>\d+)/edit/$', login_required(views.TaskUpdateView.as_view()), name='task-update'),
)

# reverse('messageset:api-task-list'),reverse('messageset:api-task-detail', kwargs={'pk': 1})
router.register(r'api/messageset/task', views.TaskViewSet, base_name='api-task')


urlpatterns += router.urls

