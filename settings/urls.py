from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from settings import BASE_DIR, ID_PHOTO_FOLDER, MEDIA_ROOT
from core.adminlte.views import  ChangePasswordView, ChangePasswordDoneView

def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret

apps_urlpatterns = patterns('',
    url(r'^member/', include('apps.member.urls')),
    url(r'^order/', include('apps.order.urls')),
    # url(r'^product/', include('apps.product.urls')),
    url(r'^customer/', include('apps.customer.urls')),
    url(r'^', include('apps.store.urls', namespace='store')),
    url(r'^', include('apps.product.urls', namespace='product')),
    url(r'^', include('core.messageset.urls', namespace='messageset')),
)
# Member frontend

# REST API
api_urlpatterns = patterns('',
    if_installed('apps.member', r'^member/', include('apps.member.api.urls')),
    if_installed('apps.order', r'^order/', include('apps.order.api.urls')),
    if_installed('apps.product', r'^product/', include('apps.product.api.urls')),
    if_installed('apps.customer', r'^customer/', include('apps.customer.api.urls')),
)


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(apps_urlpatterns)),
    url(r'^api/', include(api_urlpatterns, namespace='api')),

    # url(r'^%s/(?P<path>.*)$' % ID_PHOTO_FOLDER, 'django.views.static.serve', {'document_root': os.path.join(BASE_DIR, ID_PHOTO_FOLDER).replace('\\', '/'), 'show_indexes': False}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),


    # registration
    url(r'^auth/', include("apps.registration.urls", namespace="registration")),

    # auth
    url('^auth/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url('^auth/change-password-done/$', ChangePasswordDoneView.as_view(), name='password_change_done'),

    # for common views
    url(r'^', include('core.adminlte.urls', namespace='adminlte')),

    # for common api
    url(r'^api/v1/', include('core.api.urls', namespace='common_api')),

    # for dbsettings
    (r'^admin/settings/', include('dbsettings.urls')),

    # for js reverse
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

)
