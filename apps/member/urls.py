from django.conf.urls import url
from . import views

urlpatterns = (
    # url(r'^login/', views.member_login, name='member-login'),
    # url(r'^logout/', views.member_logout, name='member-logout'),
    url(r'^register/', views.RegisterView.as_view(), name='member-register'),
    url(r'^home/$', views.member_home, name="member-home"),
    url(r'^agent/$', views.AgentView.as_view(), name="member-agent"),
    url(r'^profile/$', views.ProfileView.as_view(), name="member-profile"),
)
