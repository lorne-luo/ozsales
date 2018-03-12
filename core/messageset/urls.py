from django.conf.urls import url
from . import views


# urls for notification
urlpatterns = [
    url(r'^notification/list/$', views.NotificationListView.as_view(), name='notification-list'),
    url(r'^notification/(?P<pk>\d+)/$', views.NotificationDetailView.as_view(), name='notification-detail'),
    url(r'^notification/(?P<pk>\d+)/edit/$', views.NotificationUpdateView.as_view(), name='notification-update'),
]

# urls for notificationcontent
urlpatterns += [
    url(r'^notification/add/$', views.NotificationContentAddView.as_view(), name='notification-add'),
    url(r'^notificationcontent/(?P<pk>\d+)/$', views.NotificationContentDetailView.as_view(), name='notificationcontent-detail'),
    # url(r'^notificationcontent/(?P<pk>\d+)/edit/$', views.NotificationContentUpdateView.as_view(), name='notificationcontent-update'),
]

# urls for sitemailcontent
urlpatterns += [
    url(r'^sitemail/add/$', views.SiteMailContentAddView.as_view(), name='sitemail-add'),
    url(r'^sitemailcontent/(?P<pk>\d+)/$', views.SiteMailContentDetailView.as_view(), name='sitemailcontent-detail'),
    url(r'^sitemailcontent/(?P<pk>\d+)/edit/$', views.SiteMailContentUpdateView.as_view(), name='sitemailcontent-update'),
]

# urls for sitemailreceive
urlpatterns += [
    url(r'^sitemail/list/$', views.SiteMailReceiveListView.as_view(), name='sitemail-list'),
    url(r'^sitemail/list/$', views.SiteMailReceiveListView.as_view(), name='sitemailreceive-list'),
    url(r'^sitemail/receive/(?P<pk>\d+)/$', views.SiteMailReceiveDetailView.as_view(), name='sitemailreceive-detail'),
]

# urls for sitemailsend
urlpatterns += [
    url(r'^sitemailsend/(?P<pk>\d+)/$', views.SiteMailSendDetailView.as_view(), name='sitemailsend-detail'),
]

# urls for task
urlpatterns += [
    url(r'^task/list/$', views.TaskListView.as_view(), name='task-list'),
    url(r'^task/(?P<pk>\d+)/$', views.TaskDetailView.as_view(), name='task-detail'),
    # url(r'^task/(?P<pk>\d+)/edit/$', views.TaskUpdateView.as_view(), name='task-update'),
]
