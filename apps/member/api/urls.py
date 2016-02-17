from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
import views


urlpatterns = patterns('',
	url(r'^profile/$', views.Profile.as_view(), name='profile'),
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token', name='login-token'),
	url(r'^groups_and_users/$', views.GroupsAndUsersList.as_view(), name='groups-and-users'),
)

router = DefaultRouter()
router.include_root_view = False
router.register(r'user', views.SellerViewSet, 'user')

urlpatterns += router.urls
