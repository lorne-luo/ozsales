from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import views as auth_views
from wagtail.contrib.wagtailsitemaps.views import sitemap

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailimages import urls as wagtailimages_urls

from apps.order.views import OrderDetailView
# from apps.wagtail.search.views import search as wagtail_search
from core.api.views import GitCommitInfoView
from core.auth_user.views import ChangePasswordView
from core import auth_user
from apps.member.forms import CustomPasswordResetForm, CustomSetPasswordForm
from apps.member.views import member_login, member_logout

def if_installed(appname, *args, **kwargs):
    ret = url(*args, **kwargs)
    if appname not in settings.INSTALLED_APPS:
        ret.resolve = lambda *args: None
    return ret


wagtail_urlpatterns = [
    # url(r'^admin/', include(wagtailadmin_urls)),
    # url(r'^documents/', include(wagtaildocs_urls)),
    # url(r'^images/', include(wagtailimages_urls)),
    # url(r'^search/$', wagtail_search, name='wagtail_search'),
    # url(r'^pages/', include(wagtail_urls)),
]

apps_urlpatterns = [
    url(r'^$', member_login,name='member-login'),
    url(r'^logout/$', member_logout,name='member-logout'),
    # url(r'^djadmin/', include(admin.site.urls)),
    url(r'^customer/', include('apps.customer.urls', namespace='customer')),
    url(r'^member/', include('apps.member.urls', namespace='member')),
    url(r'^store/', include('apps.store.urls', namespace='store')),
    url(r'^product/', include('apps.product.urls', namespace='product')),
    url(r'^order/', include('apps.order.urls', namespace='order')),
    url(r'^express/', include('apps.express.urls', namespace='express')),
    url(r'^carrier_tracker/', include('apps.carrier_tracker.urls', namespace='carrier_tracker')),
    url(r'^report/', include('apps.report.urls', namespace='report')),
    url(r'^wx/', include('apps.weixin.urls', namespace='weixin')),
    url(r'^schedule/', include('apps.schedule.urls', namespace='schedule')),
    url(r'^messageset/', include('core.messageset.urls', namespace='messageset')),
    url(r'^payments/', include('core.payments.stripe.urls', namespace='payments')),
    url(r'^(?P<schema_id>[-\w]+)/(?P<uid>[-\w]+)/$', OrderDetailView.as_view(), name='order-detail-short'),
]

# REST API
api_urlpatterns = [
    url(r'^customer/', include('apps.customer.api.urls')),
    url(r'^carrier_tracker/', include('apps.carrier_tracker.api.urls')),
    url(r'^express/', include('apps.express.api.urls')),
    url(r'^member/', include('apps.member.api.urls')),
    url(r'^order/', include('apps.order.api.urls')),
    url(r'^product/', include('apps.product.api.urls')),
    url(r'^report/', include('apps.report.api.urls')),
    url(r'^schedule/', include('apps.schedule.api.urls')),
    url(r'^messageset/', include('core.messageset.api.urls')),
    url(r'^sms/', include('core.sms.urls')),
    url(r'^version/$', GitCommitInfoView.as_view(), name='api_version'),
]

urlpatterns = wagtail_urlpatterns + apps_urlpatterns + [
    # REST API
    url(r'^api/', include(api_urlpatterns, namespace='api')),

    # auth
    url('^auth/change-password/$', ChangePasswordView.as_view(), name='change_password'),
    url('^auth/change-password-done/$', auth_user.views.ChangePasswordDoneView.as_view(), name='password_change_done'),

    # password reset
    url(r'^password/reset/$', auth_views.password_reset, {'template_name': 'adminlte/password_reset_form.html',
                                                          'email_template_name': 'adminlte/password_reset_email.html',
                                                          'password_reset_form': CustomPasswordResetForm},
        name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        {'template_name': 'adminlte/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
        {'template_name': 'adminlte/password_reset_confirm.html',
         'set_password_form': CustomSetPasswordForm},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        {'template_name': 'adminlte/password_reset_complete.html'},
        name='password_reset_complete'),

    # dbsettings
    url(r'^djadmin/settings/', include('dbsettings.urls')),

    # django-tinymce
    url(r'^tinymce/', include('tinymce.urls')),

    # Site map and robots.txt
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^sitemap\.xml$', sitemap),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'^home/', include(wagtail_urls)),
]

if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    from django.conf.urls.static import static

    urlpatterns += [
        url(r'^api/docs/$', get_swagger_view(title='OZSales API'))
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
