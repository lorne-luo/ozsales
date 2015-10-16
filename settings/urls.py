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

# Member frontend
member_urlpatterns = patterns('',
    url(r'^member/', include('apps.member.urls')),
    # if_installed('apps.customer', r'^customer/', include('apps.customer.urls', namespace='customer')),
    # if_installed('apps.product', r'^product/', include('apps.product.urls', namespace='product')),
    # if_installed('apps.order', r'^order/', include('apps.order.urls', namespace='order')),
    # if_installed('apps.store', r'^store/', include('apps.store.urls', namespace='store')),
    # if_installed('apps.common', r'^common/', include('apps.common.urls', namespace='common')),
    # if_installed('apps.express', r'^express/', include('apps.express.urls', namespace='express')),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ecosway.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^/', include(member_urlpatterns)),


    # url(r'^%s/(?P<path>.*)$' % ID_PHOTO_FOLDER, 'django.views.static.serve', {'document_root': os.path.join(BASE_DIR, ID_PHOTO_FOLDER).replace('\\', '/'), 'show_indexes': False}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    url(r'^order/(?P<order_id>\d+)/(?P<status_str>\w+)/$', 'apps.order.views.change_order_status', name='change-order-status'),
    # url('^order/', 'apps.order.urls'),
    # url('^customer/', 'customer.urls'),
    # url('^store/', 'store.urls'),
    # url('^product/', 'product.urls'),
    # url('^seller/', 'seller.urls'),
	(r'^settings/', include('dbsettings.urls')),

)

urlpatterns += staticfiles_urlpatterns()
