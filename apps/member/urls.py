from django.conf.urls import url
import views
import serializers
from apps.member.forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import views as auth_views
urlpatterns = (
    url(r'^login/', views.member_login, name='member-login'),
    url(r'^logout/', views.member_logout, name='member-logout'),
    url(r'^register/', views.RegisterView.as_view(), name='member-register'),
    url(r'^home/$', views.member_home, name="member-home"),
    url(r'^agent/$', views.AgentView.as_view(), name="member-agent"),
    url(r'^profile/$', views.ProfileView.as_view(), name="member-profile"),
    url(r'^users/$', views.seller_index, name="seller-index"),
    url(r'^user/add/$', views.CreateUser.as_view(), name="seller-add"),
    url(r'^user/edit/(?P<pk>[\d]+)/$', views.ProfileView.as_view(), name="admin-seller-edit"),
    url(r'^user/delete/(?P<pk>[-\d]+)/$', views.user_delete, name="user-delete"),
    url(r'^user/password/(?P<pk>[-\d]+)/$', views.user_password_reset, name="user-password"),
)

urlpatterns += (
    url(r'^password/reset/$', auth_views.password_reset, {'template_name': 'adminlte/password_reset_form.html',
                                                 'email_template_name':'adminlte/password_reset_email.html',
                                                 'password_reset_form': CustomPasswordResetForm}, name='password_reset'),
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
)