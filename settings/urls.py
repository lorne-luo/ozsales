from django.contrib import admin
from django.conf.urls import  include, url
from django.conf import settings
from django.contrib.staticfiles.views import serve
from dbsettings.views import site_settings, app_settings
from settings import BASE_DIR, ID_PHOTO_FOLDER, MEDIA_ROOT
from core.views.views import  ChangePasswordView, ChangePasswordDoneView

def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret

apps_urlpatterns = [
    url(r'^member/', include('apps.member.urls')),
    # url(r'^order/', include('apps.order.urls')),
    # url(r'^product/', include('apps.product.urls')),
    url(r'^customer/', include('apps.customer.urls')),
    url(r'^', include('apps.customer.urls', namespace='customer')),
    url(r'^', include('apps.member.urls', namespace='customer')),
    url(r'^', include('apps.store.urls', namespace='store')),
    url(r'^', include('apps.product.urls', namespace='product')),
    url(r'^', include('apps.order.urls', namespace='order')),
    url(r'^', include('apps.express.urls', namespace='express')),
    url(r'^', include('apps.report.urls', namespace='report')),
    url(r'^', include('apps.weixin.urls', namespace='weixin')),
    url(r'^', include('apps.schedule.urls', namespace='schedule')),
    url(r'^', include('core.messageset.urls', namespace='messageset')),
    url(r'^', include('core.payments.stripe.views', namespace='payments')),
]
# Member frontend

# REST API
api_urlpatterns = [
    if_installed('apps.member', r'^member/', include('apps.member.api.urls')),
    if_installed('apps.order', r'^order/', include('apps.order.api.urls')),
    if_installed('apps.product', r'^product/', include('apps.product.api.urls')),
    if_installed('apps.customer', r'^customer/', include('apps.customer.api.urls')),
]


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

# For Apps
    url(r'^member/', include('apps.member.urls')),
    # url(r'^order/', include('apps.order.urls')),
    # url(r'^product/', include('apps.product.urls')),
    url(r'^customer/', include('apps.customer.urls')),
    url(r'^', include('apps.customer.urls', namespace='customer')),
    url(r'^', include('apps.member.urls', namespace='member')),
    url(r'^', include('apps.store.urls', namespace='store')),
    url(r'^', include('apps.product.urls', namespace='product')),
    url(r'^', include('apps.order.urls', namespace='order')),
    url(r'^', include('apps.express.urls', namespace='express')),
    url(r'^', include('apps.report.urls', namespace='report')),
    url(r'^', include('apps.weixin.urls', namespace='weixin')),
    url(r'^', include('apps.schedule.urls', namespace='schedule')),
    url(r'^', include('core.messageset.urls', namespace='messageset')),
    url(r'^', include('core.payments.stripe.urls', namespace='payments')),

    # REST API
#     url(r'^api/', include(api_urlpatterns, namespace='api')),

    # url(r'^%s/(?P<path>.*)$' % ID_PHOTO_FOLDER, 'django.views.static.serve', {'document_root': os.path.join(BASE_DIR, ID_PHOTO_FOLDER).replace('\\', '/'), 'show_indexes': False}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),


    # registration
    # url(r'^auth/', include("apps.registration.urls", namespace="registration")),

    # auth
    url('^auth/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url('^auth/change-password-done/$', ChangePasswordDoneView.as_view(), name='password_change_done'),

    # for common views
    # url(r'^', include('core.views.urls', namespace='adminlte')),

    # for common api
    url(r'^api/v1/', include('core.api.urls', namespace='common_api')),

    # for sms api
    url(r'^', include('core.sms.urls')),

    # for dbsettings
    # (r'^admin/settings/', include('dbsettings.urls')),
    url(r'^admin/settings/$', site_settings, name='site_settings'),
    url(r'^admin/settings/(?P<app_label>[^/]+)/$', app_settings, name='app_settings'),

    # for django-tinymce
    url(r'^tinymce/', include('tinymce.urls')),

    # for js reverse
    # url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
]
