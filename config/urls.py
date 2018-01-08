from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.staticfiles.views import serve
from dbsettings.views import site_settings, app_settings

from apps.order.views import OrderDetailView
from core.auth_user.views import ChangePasswordView, ChangePasswordDoneView
from core import auth_user
from core.auth_user.views import index


def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret


apps_urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^customer/', include('apps.customer.urls', namespace='customer')),
    url(r'^member/', include('apps.member.urls', namespace='member')),
    url(r'^store/', include('apps.store.urls', namespace='store')),
    url(r'^product/', include('apps.product.urls', namespace='product')),
    url(r'^order/', include('apps.order.urls', namespace='order')),
    url(r'^(?P<customer_id>\d+)/(?P<pk>\d+)/$', OrderDetailView.as_view(), name='order-detail-short'),
    url(r'^express/', include('apps.express.urls', namespace='express')),
    url(r'^report/', include('apps.report.urls', namespace='report')),
    url(r'^wx/', include('apps.weixin.urls', namespace='weixin')),
    url(r'^schedule/', include('apps.schedule.urls', namespace='schedule')),
    url(r'^messageset/', include('core.messageset.urls', namespace='messageset')),
    url(r'^payments/', include('core.payments.stripe.urls', namespace='payments')),
]

# REST API
api_urlpatterns = [
    url(r'^customer/', include('apps.customer.api.urls')),
    url(r'^express/', include('apps.express.api.urls')),
    url(r'^member/', include('apps.member.api.urls')),
    url(r'^order/', include('apps.order.api.urls')),
    url(r'^product/', include('apps.product.api.urls')),
    url(r'^report/', include('apps.report.api.urls')),
    url(r'^schedule/', include('apps.schedule.api.urls')),
    url(r'^messageset/', include('core.messageset.api.urls')),
    url(r'^sms/', include('core.sms.urls')),
]

urlpatterns = apps_urlpatterns + [
    url(r'^$', index, name='index'),

    # REST API
    url(r'^api/', include(api_urlpatterns, namespace='api')),

    # auth
    url('^auth/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url('^auth/change-password-done/$', auth_user.views.ChangePasswordDoneView.as_view(), name='password_change_done'),

    # dbsettings
    url(r'^admin/settings/', include('dbsettings.urls')),

    # django-tinymce
    url(r'^tinymce/', include('tinymce.urls')),

]

if settings.DEBUG:
    # url(r'^%s/(?P<path>.*)$' % ID_PHOTO_FOLDER, 'django.views.static.serve', {'document_root': os.path.join(BASE_DIR, ID_PHOTO_FOLDER).replace('\\', '/'), 'show_indexes': False}),
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
