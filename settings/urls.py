from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from settings import BASE_DIR, ID_PHOTO_FOLDER, MEDIA_ROOT
from utils.custom_admin_site import member_site

def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret

apps_urlpatterns = patterns('',
    url(r'^member/', include('apps.member.urls')),
    url(r'^order/', include('apps.order.urls')),
    url(r'^product/', include('apps.product.urls')),
    url(r'^customer/', include('apps.customer.urls')),
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
    url(r'^order/(?P<order_id>\d+)/(?P<status_str>\w+)/$', 'apps.order.views.change_order_status', name='change-order-status'),

    # for common views
    url(r'^', include('apps.common.urls', namespace='common')),

    # for common api
    url(r'^api/v1/', include('apps.api.urls', namespace='common_api')),


    # for dbsettings
    (r'^admin/settings/', include('dbsettings.urls')),
)

urlpatterns += staticfiles_urlpatterns()
