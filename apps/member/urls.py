
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('apps.member.views',
    url(r'^login/', 'loginview', name='member-login'),
)

urlpatterns += patterns('django.contrib.auth.views',
   	url(r'^password_change/$', 'password_change', {'template_name': 'member/password_change_form.html'}),
	url(r'^password_change/done/$', 'password_change_done', {'template_name': 'member/password_change_done.html'}),
	url(r'^password/reset/$', 'password_reset', {'template_name': 'registration/password_reset_form.html', 'email_template_name':'email/password_reset_email_txt.html'}),
	url(r'^password/reset/done/$', 'password_reset_done', {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
	url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'password_reset_confirm', {'template_name': 'registration/password_reset_confirm.html'}),
	url(r'^password/reset/complete/$', 'password_reset_complete', {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
)