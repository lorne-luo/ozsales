from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os
from django.conf.urls import patterns, include, url
from django.contrib import admin
from settings import BASE_DIR, ID_PHOTO_FOLDER, MEDIA_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ecosway.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(admin.site.urls)),
    # url(r'^%s/(?P<path>.*)$' % ID_PHOTO_FOLDER, 'django.views.static.serve', {'document_root': os.path.join(BASE_DIR, ID_PHOTO_FOLDER).replace('\\', '/'), 'show_indexes': False}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    url(r'^order/(?P<order_id>\d+)/(?P<status_str>\w+)/$', 'apps.order.views.change_order_status', name="change-order-status"),
    # url('^order/', 'apps.order.urls'),
    # url('^customer/', 'customer.urls'),
    # url('^store/', 'store.urls'),
    # url('^product/', 'product.urls'),
    # url('^seller/', 'seller.urls'),
	(r'^settings/', include('dbsettings.urls')),
)

urlpatterns += staticfiles_urlpatterns()
